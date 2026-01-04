from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import bcrypt
import os
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Insert user into database
    try:
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT Token (Identity must be string)
        access_token = create_access_token(identity=str(new_user.id))
        
        return jsonify({
            'message': 'Registration successful',
            'token': access_token,
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email
            }
        }), 201
    except Exception as e:
        db.session.rollback()
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
    user = User.query.filter_by(username=username).first()
    
    if not user:
        # Avoid user enumeration, but basic check for now
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Verify password (encode string to bytes for bcrypt)
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Generate JWT Token
    access_token = create_access_token(identity=str(user.id))
    
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
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user"""
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
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
        user = User.query.get(int(current_user_id))
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
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    if user.email != email:
        return jsonify({'error': 'Email does not match our records'}), 401
        
    # Hash new password
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Update password in database
    try:
        user.password_hash = password_hash
        db.session.commit()
        return jsonify({'message': 'Password reset successful. You can now login.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to reset password: {str(e)}'}), 500
