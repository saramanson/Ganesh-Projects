from flask import Blueprint, request, jsonify, make_response
import io
import csv
import os
import json
import uuid
from datetime import datetime

groups_bp = Blueprint('groups', __name__)

STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')
GROUPS_FILE = os.path.join(STORAGE_DIR, 'groups.json')
FRIENDS_FILE = os.path.join(STORAGE_DIR, 'friends.json')
SHARED_EXPENSES_FILE = os.path.join(STORAGE_DIR, 'shared_expenses.json')
SETTLEMENTS_FILE = os.path.join(STORAGE_DIR, 'settlements.json')

def load_json_file(filepath, default=None):
    """Load JSON file with error handling"""
    if default is None:
        default = []
    
    if not os.path.exists(filepath):
        return default
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default

def save_json_file(filepath, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# ==================== FRIENDS ENDPOINTS ====================

@groups_bp.route('/api/friends', methods=['GET'])
def get_friends():
    """Get all friends"""
    friends = load_json_file(FRIENDS_FILE, [])
    return jsonify(friends)

@groups_bp.route('/api/friends', methods=['POST'])
def add_friend():
    """Add a new friend"""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email', '')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    friends = load_json_file(FRIENDS_FILE, [])
    
    new_friend = {
        'id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'created_at': datetime.now().isoformat()
    }
    
    friends.append(new_friend)
    save_json_file(FRIENDS_FILE, friends)
    
    return jsonify(new_friend), 201

@groups_bp.route('/api/friends/<friend_id>', methods=['DELETE'])
def delete_friend(friend_id):
    """Delete a friend"""
    friends = load_json_file(FRIENDS_FILE, [])
    original_count = len(friends)
    
    friends = [f for f in friends if f['id'] != friend_id]
    
    if len(friends) < original_count:
        save_json_file(FRIENDS_FILE, friends)
        return jsonify({'message': 'Friend deleted'})
    
    return jsonify({'error': 'Friend not found'}), 404

# ==================== GROUPS ENDPOINTS ====================

@groups_bp.route('/api/groups', methods=['GET'])
def get_groups():
    """Get all groups"""
    groups = load_json_file(GROUPS_FILE, [])
    return jsonify(groups)

@groups_bp.route('/api/groups', methods=['POST'])
def create_group():
    """Create a new group"""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    member_ids = data.get('member_ids', [])
    
    if not name:
        return jsonify({'error': 'Group name is required'}), 400
    
    groups = load_json_file(GROUPS_FILE, [])
    
    new_group = {
        'id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'member_ids': member_ids,
        'created_at': datetime.now().isoformat()
    }
    
    groups.append(new_group)
    save_json_file(GROUPS_FILE, groups)
    
    return jsonify(new_group), 201

@groups_bp.route('/api/groups/<group_id>', methods=['PUT'])
def update_group(group_id):
    """Update a group"""
    data = request.get_json()
    groups = load_json_file(GROUPS_FILE, [])
    
    for group in groups:
        if group['id'] == group_id:
            group['name'] = data.get('name', group['name'])
            group['description'] = data.get('description', group['description'])
            group['member_ids'] = data.get('member_ids', group['member_ids'])
            group['updated_at'] = datetime.now().isoformat()
            
            save_json_file(GROUPS_FILE, groups)
            return jsonify(group)
    
    return jsonify({'error': 'Group not found'}), 404

@groups_bp.route('/api/groups/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Delete a group"""
    groups = load_json_file(GROUPS_FILE, [])
    original_count = len(groups)
    
    groups = [g for g in groups if g['id'] != group_id]
    
    if len(groups) < original_count:
        save_json_file(GROUPS_FILE, groups)
        return jsonify({'message': 'Group deleted'})
    
    return jsonify({'error': 'Group not found'}), 404

# ==================== SHARED EXPENSES ENDPOINTS ====================

@groups_bp.route('/api/shared-expenses', methods=['GET'])
def get_shared_expenses():
    """Get all shared expenses, optionally filtered by group"""
    group_id = request.args.get('group_id')
    expenses = load_json_file(SHARED_EXPENSES_FILE, [])
    
    if group_id:
        expenses = [e for e in expenses if e['group_id'] == group_id]
    
    return jsonify(expenses)

@groups_bp.route('/api/shared-expenses', methods=['POST'])
def add_shared_expense():
    """Add a new shared expense"""
    data = request.get_json()
    
    description = data.get('description')
    amount = data.get('amount')
    paid_by = data.get('paid_by')  # friend_id who paid
    group_id = data.get('group_id')
    split_type = data.get('split_type', 'equal')  # equal, unequal, percentage, shares
    splits = data.get('splits', [])  # List of {friend_id, amount/percentage/shares}
    date = data.get('date', datetime.now().isoformat())
    category = data.get('category', 'General')
    
    if not all([description, amount, paid_by, group_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    # Calculate splits based on type
    calculated_splits = calculate_splits(amount, split_type, splits)
    
    expenses = load_json_file(SHARED_EXPENSES_FILE, [])
    
    new_expense = {
        'id': str(uuid.uuid4()),
        'description': description,
        'amount': amount,
        'paid_by': paid_by,
        'group_id': group_id,
        'split_type': split_type,
        'splits': calculated_splits,
        'date': date,
        'category': category,
        'created_at': datetime.now().isoformat()
    }
    
    expenses.append(new_expense)
    save_json_file(SHARED_EXPENSES_FILE, expenses)
    
    return jsonify(new_expense), 201

def calculate_splits(total_amount, split_type, splits):
    """Calculate how much each person owes based on split type"""
    calculated = []
    
    if split_type == 'equal':
        # Split equally among all participants
        num_people = len(splits)
        if num_people == 0:
            return []
        
        amount_per_person = round(total_amount / num_people, 2)
        
        for split in splits:
            calculated.append({
                'friend_id': split['friend_id'],
                'amount': amount_per_person
            })
    
    elif split_type == 'unequal':
        # Use exact amounts provided
        for split in splits:
            calculated.append({
                'friend_id': split['friend_id'],
                'amount': float(split['amount'])
            })
    
    elif split_type == 'percentage':
        # Calculate based on percentages
        for split in splits:
            percentage = float(split['percentage'])
            amount = round(total_amount * (percentage / 100), 2)
            calculated.append({
                'friend_id': split['friend_id'],
                'amount': amount
            })
    
    elif split_type == 'shares':
        # Calculate based on shares
        total_shares = sum(float(split['shares']) for split in splits)
        if total_shares == 0:
            return []
        
        for split in splits:
            shares = float(split['shares'])
            amount = round(total_amount * (shares / total_shares), 2)
            calculated.append({
                'friend_id': split['friend_id'],
                'amount': amount
            })

    elif split_type == 'full':
        # Full amount assigned to one person
        if not splits:
            return []
            
        target_id = splits[0]['friend_id']
        calculated.append({
            'friend_id': target_id,
            'amount': float(total_amount)
        })
    
    return calculated

@groups_bp.route('/api/shared-expenses/<expense_id>', methods=['DELETE'])
def delete_shared_expense(expense_id):
    """Delete a shared expense"""
    expenses = load_json_file(SHARED_EXPENSES_FILE, [])
    original_count = len(expenses)
    
    expenses = [e for e in expenses if e['id'] != expense_id]
    
    if len(expenses) < original_count:
        save_json_file(SHARED_EXPENSES_FILE, expenses)
        return jsonify({'message': 'Expense deleted'})
    
    return jsonify({'error': 'Expense not found'}), 404

# ==================== BALANCE TRACKING ====================

@groups_bp.route('/api/balances', methods=['GET'])
def get_balances():
    """Calculate balances - who owes whom"""
    group_id = request.args.get('group_id')
    
    expenses = load_json_file(SHARED_EXPENSES_FILE, [])
    settlements = load_json_file(SETTLEMENTS_FILE, [])
    
    if group_id:
        expenses = [e for e in expenses if e['group_id'] == group_id]
        settlements = [s for s in settlements if s['group_id'] == group_id]
    
    # Calculate net balances
    balances = {}  # {friend_id: {owes_to: {friend_id: amount}}}
    
    # Process expenses
    for expense in expenses:
        paid_by = expense['paid_by']
        
        for split in expense['splits']:
            friend_id = split['friend_id']
            amount = split['amount']
            
            # Skip if person paid for themselves
            if friend_id == paid_by:
                continue
            
            # Initialize nested dicts if needed
            if friend_id not in balances:
                balances[friend_id] = {}
            
            if paid_by not in balances[friend_id]:
                balances[friend_id][paid_by] = 0
            
            balances[friend_id][paid_by] += amount
    
    # Process settlements (subtract from balances)
    for settlement in settlements:
        paid_by = settlement['paid_by']
        paid_to = settlement['paid_to']
        amount = settlement['amount']
        
        if paid_by in balances and paid_to in balances[paid_by]:
            balances[paid_by][paid_to] -= amount
            
            # Remove if balance is zero or negative
            if balances[paid_by][paid_to] <= 0.01:  # Account for floating point
                del balances[paid_by][paid_to]
    
    # Simplify debts
    simplified = simplify_debts(balances)
    
    return jsonify(simplified)

def simplify_debts(balances):
    """Simplify debts to minimize number of transactions"""
    # Calculate net balance for each person
    net_balance = {}
    
    for debtor, creditors in balances.items():
        if debtor not in net_balance:
            net_balance[debtor] = 0
        
        for creditor, amount in creditors.items():
            net_balance[debtor] -= amount
            
            if creditor not in net_balance:
                net_balance[creditor] = 0
            net_balance[creditor] += amount
    
    # Separate into debtors (negative) and creditors (positive)
    debtors = [(person, -amount) for person, amount in net_balance.items() if amount < -0.01]
    creditors = [(person, amount) for person, amount in net_balance.items() if amount > 0.01]
    
    # Sort for consistent results
    debtors.sort(key=lambda x: x[1], reverse=True)
    creditors.sort(key=lambda x: x[1], reverse=True)
    
    # Create simplified transactions
    simplified = []
    
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]
        
        # Transfer minimum of debt and credit
        transfer = min(debt_amount, credit_amount)
        
        if transfer > 0.01:  # Only add if meaningful amount
            simplified.append({
                'from': debtor,
                'to': creditor,
                'amount': round(transfer, 2)
            })
        
        # Update amounts
        debtors[i] = (debtor, debt_amount - transfer)
        creditors[j] = (creditor, credit_amount - transfer)
        
        # Move to next debtor/creditor if settled
        if debtors[i][1] < 0.01:
            i += 1
        if creditors[j][1] < 0.01:
            j += 1
    
    return simplified

# ==================== SETTLEMENTS ENDPOINTS ====================

@groups_bp.route('/api/settlements', methods=['GET'])
def get_settlements():
    """Get all settlements, optionally filtered by group"""
    group_id = request.args.get('group_id')
    settlements = load_json_file(SETTLEMENTS_FILE, [])
    
    if group_id:
        settlements = [s for s in settlements if s['group_id'] == group_id]
    
    return jsonify(settlements)

@groups_bp.route('/api/settlements', methods=['POST'])
def record_settlement():
    """Record a payment/settlement"""
    data = request.get_json()
    
    paid_by = data.get('paid_by')  # friend_id who paid
    paid_to = data.get('paid_to')  # friend_id who received
    amount = data.get('amount')
    group_id = data.get('group_id')
    notes = data.get('notes', '')
    date = data.get('date', datetime.now().isoformat())
    
    if not all([paid_by, paid_to, amount, group_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    settlements = load_json_file(SETTLEMENTS_FILE, [])
    
    new_settlement = {
        'id': str(uuid.uuid4()),
        'paid_by': paid_by,
        'paid_to': paid_to,
        'amount': amount,
        'group_id': group_id,
        'notes': notes,
        'date': date,
        'created_at': datetime.now().isoformat()
    }
    
    settlements.append(new_settlement)
    save_json_file(SETTLEMENTS_FILE, settlements)
    
    return jsonify(new_settlement), 201

@groups_bp.route('/api/settlements/<settlement_id>', methods=['DELETE'])
def delete_settlement(settlement_id):
    """Delete a settlement"""
    settlements = load_json_file(SETTLEMENTS_FILE, [])
    original_count = len(settlements)
    
    settlements = [s for s in settlements if s['id'] != settlement_id]
    
    if len(settlements) < original_count:
        save_json_file(SETTLEMENTS_FILE, settlements)
        return jsonify({'message': 'Settlement deleted'})
    
    return jsonify({'error': 'Settlement not found'}), 404

@groups_bp.route('/api/groups/<group_id>/export', methods=['GET'])
def export_group_expenses(group_id):
    """Export group expenses as CSV"""
    expenses = load_json_file(SHARED_EXPENSES_FILE, [])
    expenses = [e for e in expenses if e['group_id'] == group_id]
    
    # Also need friends names to make it readable
    friends = load_json_file(FRIENDS_FILE, [])
    friend_map = {f['id']: f['name'] for f in friends}
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Description', 'Amount', 'Paid By', 'Category', 'Split Type'])
    
    for e in expenses:
        paid_by_name = friend_map.get(e['paid_by'], 'Unknown')
        cw.writerow([
            e['date'], 
            e['description'], 
            e['amount'], 
            paid_by_name, 
            e.get('category', 'General'), 
            e['split_type']
        ])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=group_expenses_{group_id}.csv"
    output.headers["Content-type"] = "text/csv"
    return output
