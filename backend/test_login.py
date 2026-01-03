import requests
import json

# Create a session to maintain cookies
session = requests.Session()

# Test login endpoint
login_url = "http://127.0.0.1:5000/api/auth/login"
login_data = {
    "username": "Ganesh",
    "password": "Letmego4awalk"
}

print("Testing login...")
try:
    response = session.post(login_url, json=login_data)
    print(f"Login Status Code: {response.status_code}")
    print(f"Login Response: {response.json()}")
    
    # Test if we can access protected endpoint
    print("\nTesting protected endpoint (get transactions)...")
    transactions_url = "http://127.0.0.1:5000/api/transactions"
    trans_response = session.get(transactions_url)
    print(f"Transactions Status Code: {trans_response.status_code}")
    print(f"Transactions Response: {trans_response.json()}")
    
except Exception as e:
    print(f"Error: {e}")
