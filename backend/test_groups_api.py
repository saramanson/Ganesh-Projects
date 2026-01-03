import requests
import json
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


BASE_URL = "http://127.0.0.1:5000/api"

def test_groups_api():
    print("=" * 60)
    print("Testing Expense Splitting API")
    print("=" * 60)
    
    # Test 1: Add Friends
    print("\n1. Adding friends...")
    friends = []
    for name, email in [("Alice", "alice@example.com"), ("Bob", "bob@example.com"), ("Charlie", "charlie@example.com")]:
        response = requests.post(f"{BASE_URL}/friends", json={"name": name, "email": email})
        if response.status_code == 201:
            friend = response.json()
            friends.append(friend)
            print(f"   ✓ Added {name} (ID: {friend['id'][:8]}...)")
        else:
            print(f"   ✗ Failed to add {name}")
            return
    
    # Test 2: Get Friends
    print("\n2. Fetching all friends...")
    response = requests.get(f"{BASE_URL}/friends")
    if response.status_code == 200:
        all_friends = response.json()
        print(f"   ✓ Found {len(all_friends)} friends")
    else:
        print("   ✗ Failed to fetch friends")
        return
    
    # Test 3: Create Group
    print("\n3. Creating a group...")
    group_data = {
        "name": "Weekend Trip",
        "description": "Vegas 2024",
        "member_ids": [f['id'] for f in friends]
    }
    response = requests.post(f"{BASE_URL}/groups", json=group_data)
    if response.status_code == 201:
        group = response.json()
        print(f"   ✓ Created group '{group['name']}' (ID: {group['id'][:8]}...)")
        print(f"   ✓ Members: {len(group['member_ids'])}")
    else:
        print("   ✗ Failed to create group")
        return
    
    # Test 4: Add Shared Expense (Equal Split)
    print("\n4. Adding shared expense (equal split)...")
    expense_data = {
        "description": "Hotel Room",
        "amount": 300,
        "paid_by": friends[0]['id'],  # Alice paid
        "group_id": group['id'],
        "split_type": "equal",
        "splits": [{"friend_id": f['id']} for f in friends],
        "category": "Accommodation"
    }
    response = requests.post(f"{BASE_URL}/shared-expenses", json=expense_data)
    if response.status_code == 201:
        expense = response.json()
        print(f"   ✓ Added expense: {expense['description']} - ${expense['amount']}")
        print(f"   ✓ Split type: {expense['split_type']}")
        for split in expense['splits']:
            print(f"      - ${split['amount']:.2f} per person")
            break
    else:
        print("   ✗ Failed to add expense")
        return
    
    # Test 5: Add Another Expense (Unequal Split)
    print("\n5. Adding shared expense (unequal split)...")
    expense_data = {
        "description": "Dinner",
        "amount": 90,
        "paid_by": friends[1]['id'],  # Bob paid
        "group_id": group['id'],
        "split_type": "unequal",
        "splits": [
            {"friend_id": friends[0]['id'], "amount": 40},
            {"friend_id": friends[1]['id'], "amount": 30},
            {"friend_id": friends[2]['id'], "amount": 20}
        ],
        "category": "Food"
    }
    response = requests.post(f"{BASE_URL}/shared-expenses", json=expense_data)
    if response.status_code == 201:
        expense = response.json()
        print(f"   ✓ Added expense: {expense['description']} - ${expense['amount']}")
        print(f"   ✓ Split type: {expense['split_type']}")
    else:
        print("   ✗ Failed to add expense")
        return
    
    # Test 6: Get Balances
    print("\n6. Calculating balances...")
    response = requests.get(f"{BASE_URL}/balances?group_id={group['id']}")
    if response.status_code == 200:
        balances = response.json()
        print(f"   ✓ Simplified balances calculated")
        if balances:
            for balance in balances:
                # Get friend names
                from_name = next((f['name'] for f in friends if f['id'] == balance['from']), 'Unknown')
                to_name = next((f['name'] for f in friends if f['id'] == balance['to']), 'Unknown')
                print(f"      {from_name} → {to_name}: ${balance['amount']:.2f}")
        else:
            print("      All settled up!")
    else:
        print("   ✗ Failed to get balances")
        return
    
    # Test 7: Record Settlement
    print("\n7. Recording a settlement...")
    if balances:
        settlement_data = {
            "paid_by": balances[0]['from'],
            "paid_to": balances[0]['to'],
            "amount": balances[0]['amount'],
            "group_id": group['id'],
            "notes": "Cash payment"
        }
        response = requests.post(f"{BASE_URL}/settlements", json=settlement_data)
        if response.status_code == 201:
            settlement = response.json()
            print(f"   ✓ Recorded settlement: ${settlement['amount']:.2f}")
        else:
            print("   ✗ Failed to record settlement")
            return
    
    # Test 8: Get Updated Balances
    print("\n8. Checking updated balances...")
    response = requests.get(f"{BASE_URL}/balances?group_id={group['id']}")
    if response.status_code == 200:
        balances = response.json()
        print(f"   ✓ Updated balances calculated")
        if balances:
            for balance in balances:
                from_name = next((f['name'] for f in friends if f['id'] == balance['from']), 'Unknown')
                to_name = next((f['name'] for f in friends if f['id'] == balance['to']), 'Unknown')
                print(f"      {from_name} → {to_name}: ${balance['amount']:.2f}")
        else:
            print("      All settled up! 🎉")
    else:
        print("   ✗ Failed to get balances")
        return
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Open http://localhost:5173 in your browser")
    print("2. Click '👥 Split Expenses' in the navigation")
    print("3. Start managing groups and splitting expenses!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_groups_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the backend server")
        print("Please make sure the Flask server is running on http://127.0.0.1:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
