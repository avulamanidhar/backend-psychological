import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000/api/"

def verify_backend():
    print("\n=== MindGuard Auth Verification ===")
    
    # 1. Register a new user
    timestamp = int(time.time())
    username = f"auth_test_{timestamp}"
    password = "testpassword123"
    email = f"{username}@example.com"
    
    print(f"\n[1] Registering user: {username}...")
    reg_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{BASE_URL}users/", json=reg_payload)
        print(f"Status: {response.status_code}")
        if response.status_code != 201:
            print(f"Registration failed: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is 'python manage.py runserver' running?")
        return

    # 2. Test Login
    print(f"\n[2] Testing Login with: {username}...")
    login_payload = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}login/", json=login_payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Login Successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Login Failed: {response.text}")

    # 3. Test Forgot Password
    print(f"\n[3] Testing Forgot Password for: {username}...")
    forgot_payload = {
        "username": username
    }
    response = requests.post(f"{BASE_URL}forgot-password/", json=forgot_payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Forgot Password logic working!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Forgot Password Failed: {response.text}")

    # 4. Test Invalid Login
    print(f"\n[4] Testing Invalid Login...")
    bad_login_payload = {
        "username": username,
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}login/", json=bad_login_payload)
    print(f"Status: {response.status_code} (Expected 401)")
    if response.status_code == 401:
        print("Invalid login handled correctly.")
    else:
        print(f"Unexpected status: {response.status_code}")

if __name__ == "__main__":
    verify_backend()
