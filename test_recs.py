import requests
import random
import time

BASE_URL = "http://127.0.0.1:8000/api/"

def test_recommendations():
    num = random.randint(1000, 9999)
    username = f"rec_user_{num}"
    
    # 1. Register
    reg_resp = requests.post(f"{BASE_URL}users/", json={
        "username": username,
        "password": "password123",
        "email": f"{username}@test.com"
    })
    print(f"Register: {reg_resp.status_code}")
    
    # 2. Login
    login_resp = requests.post(f"{BASE_URL}login/", json={
        "username": username,
        "password": "password123"
    })
    print(f"Login: {login_resp.status_code}")
    token = login_resp.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Recommendations
    print("Testing Recommendations...")
    recs_resp = requests.get(f"{BASE_URL}recommendations/", headers=headers)
    print(f"Status: {recs_resp.status_code}")
    if recs_resp.status_code == 200:
        recommendations = recs_resp.json()
        print(f"Count: {len(recommendations)}")
        for r in recommendations:
            print(f"- {r['title']} ({r['type']})")
    else:
        print(f"Failed: {recs_resp.text}")

if __name__ == "__main__":
    test_recommendations()
