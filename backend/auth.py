from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import bcrypt
import sqlite3
import os

auth_bp = Blueprint('auth', __name__)

# Database setup
# Use the same storage directory as app.py for persistence
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')
DB_PATH = os.path.join(STORAGE_DIR, 'users.db')

def init_db():
    # Ensure storage directory exists
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on module load
init_db()

class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

def get_user_by_username(username):
    """Get user by username"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, password_hash FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def get_user_by_email(email):
    """Get user by email"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE email = ?', (email,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Ensure DB is initialized before first write (Render ephemeral storage fix)
    init_db()
    
    # Validation
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user already exists
    if get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400
    
    if get_user_by_email(email):
        return jsonify({'error': 'Email already exists'}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert user into database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        # Create user object
        user = User(user_id, username, email)
        
        # Generate JWT Token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Registration successful',
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Get user from database
    user_data = get_user_by_username(username)
    
    if not user_data:
        # Avoid user enumeration, but basic check for now
        return jsonify({'error': 'Invalid username or password'}), 401
    
    user_id, username, email, password_hash = user_data
    
    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create user object
    user = User(user_id, username, email)
    
    # Generate JWT Token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    # Client side just needs to discard token. 
    # With JWT cookies we'd unset them. 
    # Here we can just return success, client clears localStorage.
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user"""
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    if not user:
         return jsonify({'error': 'User not found'}), 404
         
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@auth_bp.route('/api/auth/check', methods=['GET'])
@jwt_required(optional=True)
def check_auth():
    """Check if user is authenticated"""
    current_user_id = get_jwt_identity()
    if current_user_id:
        user = get_user_by_id(current_user_id)
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }), 200
    return jsonify({'authenticated': False}), 200

@auth_bp.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Reset user password"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    new_password = data.get('newPassword')
    
    if not username or not email or not new_password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
    # Verify user exists and email matches
    user_data = get_user_by_username(username)
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
        
    user_id, db_username, db_email, _ = user_data
    
    if db_email != email:
        return jsonify({'error': 'Email does not match our records'}), 401
        
    # Hash new password
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    # Update password in database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET password_hash = ? WHERE id = ?',
            (password_hash, user_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Password reset successful. You can now login.'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to reset password: {str(e)}'}), 500
