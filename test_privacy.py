import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/"

def test_privacy():
    # 1. Fetch Policy
    p_resp = requests.get(f"{BASE_URL}privacy-policy/")
    print(f"Policy status: {p_resp.status_code}")
    if p_resp.status_code == 200:
        print(f"Policy: {p_resp.json()}")

    # 2. Register with consent
    t = int(time.time())
    username = f"privacy_user_{t}"
    payload = {
        "username": username,
        "password": "password123",
        "email": f"{username}@test.com",
        "privacy_consent_accepted": True,
        "essential_data_processing": True,
        "anonymous_analytics": True,
        "privacy_policy_version": "1.0.0"
    }
    reg_resp = requests.post(f"{BASE_URL}users/", json=payload)
    print(f"Register status: {reg_resp.status_code}")
    
    if reg_resp.status_code == 201:
        # 3. Login
        login_resp = requests.post(f"{BASE_URL}login/", json={
            "username": username,
            "password": "password123"
        })
        token = login_resp.json()['access']
        
        # 4. Check Profile
        prof_resp = requests.get(f"{BASE_URL}profile/{username}/", headers={"Authorization": f"Bearer {token}"})
        print(f"Profile: {prof_resp.json()}")
        p = prof_resp.json()
        assert p['privacy_consent_accepted'] == True
        assert p['anonymous_analytics'] == True
        print("Verification SUCCESS")

if __name__ == "__main__":
    test_privacy()
