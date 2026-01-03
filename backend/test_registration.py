import requests
import json

# Test registration endpoint
url = "http://127.0.0.1:5000/api/auth/register"
data = {
    "username": "Ganesh",
    "email": "ganeashen@gmail.com",
    "password": "Letmego4awalk"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"Error: {e}")
