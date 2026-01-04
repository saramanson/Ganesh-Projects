import requests
import json
import sys

# Production URL
BASE_URL = "https://expense-tracker-backend-hxst.onrender.com/api"
ORIGIN = "https://expense-tracker-frontend-hys6.onrender.com"

print(f"Probing {BASE_URL}...")

try:
    # 1. Check Auth Status (GET)
    print("1. Checking Status...")
    res = requests.get(f"{BASE_URL}/auth/check", headers={"Origin": ORIGIN})
    print(f"   Status: {res.status_code}")
    print(f"   Body: {res.text[:200]}...") # Print first 200 chars

    # 2. Try Registration (POST)
    print("\n2. Attempting Registration (Probe)...")
    # Use a random user to avoid 'already exists' if db is persistent
    import uuid
    random_user = f"probe_{str(uuid.uuid4())[:8]}"
    
    data = {
        "username": random_user,
        "email": f"{random_user}@example.com",
        "password": "password123"
    }
    
    headers = {
        "Origin": ORIGIN,
        "Content-Type": "application/json"
    }
    
    res = requests.post(f"{BASE_URL}/auth/register", json=data, headers=headers)
    
    print(f"   Status: {res.status_code}")
    if res.status_code != 201:
        print("   !!! ERROR DETECTED !!!")
        print("   Full Response Body:")
        print(res.text) # This is key to finding the 500 error cause
    else:
        print("   Success! (201 Created)")

except Exception as e:
    print(f"Exception: {e}")
