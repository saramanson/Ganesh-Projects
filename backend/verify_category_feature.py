import requests
import sys
import os
import json

BASE_URL = "http://127.0.0.1:5000/api/transactions"

def test_category_feature():
    print("Testing Category Feature...")
    
    # 1. Add Transaction with Category
    payload = {
        "description": "Medicine Test",
        "amount": 50,
        "type": "debit",
        "date": "2024-06-01",
        "category": "Medicine"
    }
    try:
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"Added transaction: {data['id']} with Category: {data['category']}")
        if data['category'] != "Medicine":
            print("Error: Category mismatch in response")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to add transaction: {e}")
        sys.exit(1)

    # 2. Verify GET returns category
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        transactions = response.json()
        found = False
        for t in transactions:
            if t['id'] == data['id']:
                if t.get('category') == "Medicine":
                    found = True
                    print("GET /transactions returned correct category.")
                else:
                    print(f"Error: Category missing or incorrect in GET: {t}")
                    sys.exit(1)
                break
        if not found:
            print("Transaction not found in list")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to get transactions: {e}")
        sys.exit(1)

    print("Category feature verification successful!")

if __name__ == "__main__":
    test_category_feature()
