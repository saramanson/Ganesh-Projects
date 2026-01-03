import requests
import sys
import os
import json
import time

BASE_URL = "http://127.0.0.1:5000/api/transactions"
STORAGE_DIR = "storage"

def test_date_feature():
    print("Testing Date Feature & Folder Storage...")
    
    # 1. Add Transaction for 2024
    payload_2024 = {
        "description": "2024 Transaction",
        "amount": 100,
        "type": "credit",
        "date": "2024-05-20"
    }
    try:
        response = requests.post(BASE_URL, json=payload_2024)
        response.raise_for_status()
        data_2024 = response.json()
        print(f"Added 2024 transaction: {data_2024['id']}")
    except Exception as e:
        print(f"Failed to add 2024 transaction: {e}")
        sys.exit(1)

    # 2. Add Transaction for 2025
    payload_2025 = {
        "description": "2025 Transaction",
        "amount": 50,
        "type": "debit",
        "date": "2025-01-15"
    }
    try:
        response = requests.post(BASE_URL, json=payload_2025)
        response.raise_for_status()
        data_2025 = response.json()
        print(f"Added 2025 transaction: {data_2025['id']}")
    except Exception as e:
        print(f"Failed to add 2025 transaction: {e}")
        sys.exit(1)

    # 3. Verify Folders and Files
    if not os.path.exists(os.path.join(STORAGE_DIR, "2024", "transactions.json")):
        print("Error: 2024 folder/file not found!")
        sys.exit(1)
    
    if not os.path.exists(os.path.join(STORAGE_DIR, "2025", "transactions.json")):
        print("Error: 2025 folder/file not found!")
        sys.exit(1)
        
    print("Folders and files verified.")

    # 4. Verify GET returns both
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        transactions = response.json()
        ids = [t['id'] for t in transactions]
        if data_2024['id'] in ids and data_2025['id'] in ids:
            print("GET /transactions returned both transactions.")
        else:
            print("Error: GET /transactions missing data.")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to get transactions: {e}")
        sys.exit(1)

    print("Date feature verification successful!")

if __name__ == "__main__":
    test_date_feature()
