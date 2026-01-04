import requests
import json
import sys

# Production URL
BASE_URL = "https://expense-tracker-backend-hxst.onrender.com/api"
ORIGIN = "https://expense-tracker-frontend-hys6.onrender.com"

def debug_jwt_flow():
    print(f"Debugging JWT Flow on {BASE_URL}...")
    
    # 1. Register a new user to get a FRESH token
    import uuid
    random_user = f"jwt_debug_{str(uuid.uuid4())[:8]}"
    print(f"1. Registering {random_user}...")
    
    reg_data = {
        "username": random_user,
        "email": f"{random_user}@jwt.com",
        "password": "password123"
    }
    
    res = requests.post(
        f"{BASE_URL}/auth/register", 
        json=reg_data, 
        headers={"Origin": ORIGIN, "Content-Type": "application/json"}
    )
    
    if res.status_code != 201:
        print(f"   Registration Failed: {res.status_code}")
        print(res.text)
        return

    data = res.json()
    token = data.get('token')
    print(f"   Got Token: {token[:20]}..." if token else "   NO TOKEN IN RESPONSE")
    
    if not token:
        return

    # 2. Add Transaction using the Token
    print("\n2. Adding Transaction with Token...")
    trans_data = {
        "description": "Debug Item",
        "amount": 100,
        "type": "debit",
        "date": "2026-01-04",
        "category": "Test"
    }
    
    headers = {
        "Origin": ORIGIN,
        "Authorization": f"Bearer {token}",  # Correct format
        "Content-Type": "application/json"
    }
    
    # Intentionally trying the JSON path first
    res = requests.post(f"{BASE_URL}/transactions", json=trans_data, headers=headers)
    
    print(f"   Status: {res.status_code}")
    print(f"   Response: {res.text}")
    
    if res.status_code == 422:
        print("\n   !!! 422 ERROR ANALYZED !!!")
        try:
            err = res.json()
            print(f"   Error Message: {err.get('msg', 'Unknown')}")
        except:
            print("   Could not parse JSON error.")

if __name__ == "__main__":
    debug_jwt_flow()
