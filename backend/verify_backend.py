import requests
import sys

BASE_URL = "http://127.0.0.1:5000/api/transactions"

def test_backend():
    print("Testing Backend...")
    
    # 1. Add Transaction
    payload = {
        "description": "Test Salary",
        "amount": 5000,
        "type": "credit"
    }
    try:
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"Added transaction: {data}")
        tx_id = data['id']
    except Exception as e:
        print(f"Failed to add transaction: {e}")
        sys.exit(1)

    # 2. Get Transactions
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        transactions = response.json()
        print(f"Fetched {len(transactions)} transactions")
        found = False
        for t in transactions:
            if t['id'] == tx_id:
                found = True
                break
        if not found:
            print("Transaction not found in list")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to get transactions: {e}")
        sys.exit(1)

    # 3. Delete Transaction
    try:
        response = requests.delete(f"{BASE_URL}/{tx_id}")
        response.raise_for_status()
        print("Deleted transaction")
    except Exception as e:
        print(f"Failed to delete transaction: {e}")
        sys.exit(1)

    print("Backend verification successful!")

if __name__ == "__main__":
    test_backend()
