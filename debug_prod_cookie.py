import requests

# Production URL
BASE_URL = "https://expense-tracker-backend-hxst.onrender.com/api"
ORIGIN = "https://expense-tracker-frontend-hys6.onrender.com"

def debug_cookies():
    print(f"Debugging Cookies from {BASE_URL}...")
    
    session = requests.Session()
    # mimic the frontend
    headers = {
        "Origin": ORIGIN,
        "Content-Type": "application/json"
    }
    
    # 1. Login to get a cookie
    login_data = {
        "username": "Nisha", 
        "password": "password123" # assuming this reset password or use a known one. 
        # Actually I can't guess the password. 
        # I'll try to register a temp user to get the cookie.
    }
    
    import uuid
    random_user = f"debug_{str(uuid.uuid4())[:8]}"
    reg_data = {
        "username": random_user,
        "email": f"{random_user}@test.com",
        "password": "password123"
    }
    
    print(f"1. Registering {random_user}...")
    res = session.post(f"{BASE_URL}/auth/register", json=reg_data, headers=headers)
    print(f"   Status: {res.status_code}")
    
    if res.status_code not in [200, 201]:
        print("   Registration failed, cannot check cookies.")
        print(res.text)
        return

    # Check the cookie in the jar
    print("2. Inspecting Cookies...")
    if not session.cookies:
        print("   NO COOKIES RECEIVED!")
        return
        
    for cookie in session.cookies:
        print(f"   Name: {cookie.name}")
        print(f"   Domain: {cookie.domain}")
        print(f"   Path: {cookie.path}")
        print(f"   Secure: {cookie.secure}")
        # Requests cookie jar doesn't always expose SameSite easily, but we can check headers
        
    print("\n3. Inspecting Headers for Set-Cookie...")
    set_cookie = res.headers.get('Set-Cookie')
    print(f"   Set-Cookie Raw: {set_cookie}")
    
    if 'SameSite=None' in set_cookie and 'Secure' in set_cookie:
        print("   [PASS] Configuration looks CORRECT for Cross-Site.")
    else:
        print("   [FAIL] Configuration matches LOCAL/DEV (Lax/Missing Secure).")

if __name__ == "__main__":
    debug_cookies()
