import requests
import sys
import os
import json

BASE_URL = "http://127.0.0.1:5000/api/transactions"

def test_chart_logic():
    print("Testing Chart Logic (Data Aggregation)...")
    
    # 1. Get All Transactions
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        transactions = response.json()
        print(f"Fetched {len(transactions)} transactions")
    except Exception as e:
        print(f"Failed to get transactions: {e}")
        sys.exit(1)

    # 2. Filter for Expenses (Debit)
    expenses = [t for t in transactions if t['type'] == 'debit']
    print(f"Total Expenses: {len(expenses)}")

    # 3. Group by Category
    expenses_by_category = {}
    for t in expenses:
        category = t.get('category', 'Uncategorized')
        amount = t['amount']
        expenses_by_category[category] = expenses_by_category.get(category, 0) + amount

    print("Expenses by Category:")
    for cat, amount in expenses_by_category.items():
        print(f"  {cat}: ${amount}")

    # 4. Verify Specific Data Point (from previous seed)
    # We seeded "Grocery" with 50 in 2024 Feb
    if "Grocery" in expenses_by_category:
        if expenses_by_category["Grocery"] >= 50:
            print("Verification Successful: Grocery expense found.")
        else:
             print("Error: Grocery expense amount incorrect.")
             sys.exit(1)
    else:
        print("Error: Grocery category not found in expenses.")
        # Only fail if we are sure data exists (which we are from previous steps)
        sys.exit(1)

    print("Chart logic verification successful!")

if __name__ == "__main__":
    test_chart_logic()
