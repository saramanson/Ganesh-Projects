import requests
import sys
import os
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api/transactions"

def test_sidebar_logic():
    print("Testing Sidebar Logic (Data Availability)...")
    
    # 0. Seed Data
    seed_data = [
        {"description": "2024 Jan", "amount": 100, "type": "credit", "date": "2024-01-15", "category": "Salary"},
        {"description": "2024 Feb", "amount": 50, "type": "debit", "date": "2024-02-20", "category": "Grocery"},
        {"description": "2025 Mar", "amount": 200, "type": "credit", "date": "2025-03-10", "category": "Bonus"},
    ]
    
    print("Seeding data...")
    for t in seed_data:
        try:
            requests.post(BASE_URL, json=t)
        except Exception as e:
            print(f"Failed to seed data: {e}")
            sys.exit(1)

    # 1. Get All Transactions
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        transactions = response.json()
        print(f"Fetched {len(transactions)} transactions")
    except Exception as e:
        print(f"Failed to get transactions: {e}")
        sys.exit(1)

    # 2. Extract Years
    years = set()
    for t in transactions:
        year = t['date'].split('-')[0]
        years.add(year)
    
    print(f"Available Years: {sorted(list(years))}")
    
    if "2024" not in years or "2025" not in years:
        print("Error: Expected years 2024 and 2025 not found.")
        sys.exit(1)

    # 3. Simulate Filtering for a Year
    target_year = "2024"
    filtered_by_year = [t for t in transactions if t['date'].startswith(target_year)]
    print(f"Transactions in {target_year}: {len(filtered_by_year)}")
    
    if len(filtered_by_year) < 2:
        print(f"Error: Expected at least 2 transactions for {target_year}")
        sys.exit(1)

    # 4. Simulate Filtering for a Month
    target_month = "01" # January
    filtered_by_month = [t for t in filtered_by_year if t['date'].split('-')[1] == target_month]
    print(f"Transactions in {target_year}-{target_month}: {len(filtered_by_month)}")
    
    if len(filtered_by_month) < 1:
         print(f"Error: Expected at least 1 transaction for {target_year}-{target_month}")
         sys.exit(1)

    print("Sidebar data availability verification successful!")

if __name__ == "__main__":
    test_sidebar_logic()
