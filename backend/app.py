from flask import Flask, request, jsonify, send_from_directory, make_response
import io
import csv
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
import os
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from groups_api import groups_bp
from auth import auth_bp, get_user_by_id

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# ProxyFix is required for Render to properly detect HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Secure Cookie Settings - Critical for Cross-Site (Frontend vs Backend domains)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# Get allowed origins from environment variable or default to local development
# Get allowed origins from environment variable or default to local development + specific Render frontend
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,https://expense-tracker-frontend-hys6.onrender.com').split(',')

CORS(app, supports_credentials=True, origins=allowed_origins)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.unauthorized_handler
def unauthorized():
    print(f"DEBUG: Unauthorized access. Headers: {request.headers}")
    print(f"DEBUG: Cookies: {request.cookies}")
    return jsonify({'error': 'Unauthorized', 'message': 'Please log in again'}), 401

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(groups_bp)

STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def get_user_storage_dir(user_id):
    """Get storage directory for a specific user"""
    user_dir = os.path.join(STORAGE_DIR, f'user_{user_id}')
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

def get_year_from_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        return str(dt.year)
    except ValueError:
        # Fallback if date format is just YYYY-MM-DD
        return date_str.split('-')[0]

def load_transactions(year, user_id):
    user_dir = get_user_storage_dir(user_id)
    year_dir = os.path.join(user_dir, year)
    file_path = os.path.join(year_dir, 'transactions.json')
    
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_transactions(year, transactions, user_id):
    user_dir = get_user_storage_dir(user_id)
    year_dir = os.path.join(user_dir, year)
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)
    
    file_path = os.path.join(year_dir, 'transactions.json')
    with open(file_path, 'w') as f:
        json.dump(transactions, f, indent=4)

@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    all_transactions = []
    user_dir = get_user_storage_dir(current_user.id)
    
    if os.path.exists(user_dir):
        for year_folder in os.listdir(user_dir):
            year_path = os.path.join(user_dir, year_folder)
            if os.path.isdir(year_path):
                transactions = load_transactions(year_folder, current_user.id)
                all_transactions.extend(transactions)
    
    # Sort by date descending
    all_transactions.sort(key=lambda x: x['date'], reverse=True)
    return jsonify(all_transactions)

@app.route('/api/transactions', methods=['POST'])
@login_required
def add_transaction():
    print(f"DEBUG: Received add_transaction request. Content-Type: {request.content_type}")
    print(f"DEBUG: Cookies received: {request.cookies}")
    # Check if it's a multipart/form-data request (with file) or JSON
    if request.content_type.startswith('multipart/form-data'):
        description = request.form.get('description')
        amount = request.form.get('amount')
        type = request.form.get('type')
        date = request.form.get('date')
        category = request.form.get('category')
        image_file = request.files.get('image')
    else:
        data = request.get_json()
        description = data.get('description')
        amount = data.get('amount')
        type = data.get('type')
        date = data.get('date')
        category = data.get('category')
        image_file = None

    if not description or not amount or not type or not date or not category:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    year = get_year_from_date(date)
    
    image_path = None
    if image_file:
        filename = secure_filename(image_file.filename)
        # Create images directory for the year if it doesn't exist
        user_dir = get_user_storage_dir(current_user.id)
        images_dir = os.path.join(user_dir, year, 'images')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        # Save file
        # Use a unique name to prevent overwrites if needed, or just use original
        unique_filename = f"{uuid.uuid4()}_{filename}"
        save_path = os.path.join(images_dir, unique_filename)
        image_file.save(save_path)
        
        # Store relative path: user_id/year/images/filename
        image_path = f"user_{current_user.id}/{year}/images/{unique_filename}"

    transactions = load_transactions(year, current_user.id)
    
    new_transaction = {
        'id': str(uuid.uuid4()),
        'description': description,
        'amount': amount,
        'type': type,
        'date': date,
        'category': category,
        'image': image_path
    }
    
    transactions.append(new_transaction)
    try:
        save_transactions(year, transactions, current_user.id)
        print(f"DEBUG: Successfully saved transaction {new_transaction['id']} to {year}")
    except Exception as e:
        print(f"DEBUG: Error saving transaction: {str(e)}")
        return jsonify({'error': 'Failed to save transaction'}), 500

    return jsonify(new_transaction), 201

@app.route('/api/transactions/<id>', methods=['DELETE'])
@login_required
def delete_transaction(id):
    # We need to find which year folder contains this transaction
    user_dir = get_user_storage_dir(current_user.id)
    if os.path.exists(user_dir):
        for year_folder in os.listdir(user_dir):
            year_path = os.path.join(user_dir, year_folder)
            if os.path.isdir(year_path):
                transactions = load_transactions(year_folder, current_user.id)
                
                # Filter out the transaction with the given ID
                original_count = len(transactions)
                
                # Optional: Delete associated image file if we want to clean up
                # For now, we'll keep it simple and just remove the record
                
                transactions = [t for t in transactions if t['id'] != id]
                
                if len(transactions) < original_count:
                    save_transactions(year_folder, transactions, current_user.id)
                    return jsonify({'message': 'Transaction deleted'})

    return jsonify({'error': 'Transaction not found'}), 404

@app.route('/api/storage/<path:filename>')
def serve_storage(filename):
    return send_from_directory(STORAGE_DIR, filename)

@app.route('/api/transactions/export', methods=['GET'])
@login_required
def export_transactions():
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not year:
        return jsonify({'error': 'Year is required'}), 400
        
    transactions = load_transactions(year, current_user.id)
    
    if month:
        # Filter by month (format YYYY-MM-DD where MM matches)
        transactions = [t for t in transactions if t['date'].startswith(f"{year}-{month.zfill(2)}")]
        
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Description', 'Category', 'Type', 'Amount'])
    
    for t in transactions:
        cw.writerow([t['date'], t['description'], t.get('category', ''), t['type'], t['amount']])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=transactions_{year}_{month if month else 'all'}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True, port=5000)
