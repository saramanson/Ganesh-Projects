import sqlite3
import json
import os
import uuid
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')
STORAGE_DIR = os.path.join(BASE_DIR, 'storage')
FRIENDS_FILE = os.path.join(STORAGE_DIR, 'friends.json')
GROUPS_FILE = os.path.join(STORAGE_DIR, 'groups.json')

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def fix_data():
    print("--- Starting Fix ---")

    # 1. Get Main User "Ganesh" from DB
    target_username = "Ganesh"
    print(f"Looking for user '{target_username}' in database...")
    
    if not os.path.exists(DB_PATH):
        print("Error: users.db not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (target_username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        print(f"User '{target_username}' not found in DB. Please register first.")
        return

    # User schema might vary, just get critical fields by index
    # Standard: id (0), username (1), email (2)
    username = user[1]
    email = user[2]
    print(f"Found User: {username} ({email})")

    # 2. Ensure "Ganesh" exists in friends.json
    print("Checking friends.json...")
    friends = load_json(FRIENDS_FILE)
    
    # Case-insensitive check
    friend_match = None
    for f in friends:
        if f['name'].lower() == username.lower():
            friend_match = f
            break
    
    if friend_match:
        print(f"User '{username}' already exists as a Friend (ID: {friend_match['id']})")
        friend_id = friend_match['id']
    else:
        print(f"Making '{username}' a Friend...")
        friend_id = str(uuid.uuid4())
        new_friend = {
            'id': friend_id,
            'name': username,
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        friends.append(new_friend)
        save_json(FRIENDS_FILE, friends)
        print(f"Created Friend '{username}' (ID: {friend_id})")

    # 3. Add to "Home 2026" Group
    print("Checking groups.json...")
    groups = load_json(GROUPS_FILE)
    
    group_found = False
    for group in groups:
        print(f"Processing group: '{group['name']}'")
        group_found = True
        
        if friend_id in group['member_ids']:
            print(f"'{username}' is already a member of '{group['name']}'.")
        else:
            print(f"Adding '{username}' to group '{group['name']}'...")
            group['member_ids'].append(friend_id)
            save_json(GROUPS_FILE, groups)
            print(f"Successfully added '{username}' to '{group['name']}'.")
    
    if not group_found:
        print("Group 'Home 2026' not found. Please create it first.")

    print("--- Fix Complete ---")

if __name__ == "__main__":
    fix_data()
