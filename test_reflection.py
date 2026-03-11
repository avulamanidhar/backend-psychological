import requests

BASE_URL = "http://127.0.0.1:8000/api/"

def test_reflection():
    print("Testing Reflection Generation Endpoint...")
    payload = {
        "moodName": "Anxious",
        "intensity": 85,
        "triggers": ["Work", "Health"]
    }
    resp = requests.post(f"{BASE_URL}reflection-generator/", json=payload)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Generated Reflection: {data['aiReflection']}")
        assert "anxious" in data['aiReflection'].lower()
        assert "high" in data['aiReflection'].lower()
        assert "Work" in data['aiReflection']
        assert "Health" in data['aiReflection']
    
    print("\nTesting Auto-Generation during Mood Creation...")
    # Register/Login to get token
    # (Using existing user from previous tests or creating new one)
    import time
    user = f"reflect_user_{int(time.time())}"
    requests.post(f"{BASE_URL}users/", json={"username": user, "password": "password123", "email": f"{user}@test.com"})
    login_resp = requests.post(f"{BASE_URL}login/", json={"username": user, "password": "password123"})
    token = login_resp.json()['access']
    
    mood_payload = {
        "id": f"id_{int(time.time())}",
        "timestampMillis": int(time.time() * 1000),
        "moodName": "Joyful",
        "moodImageResId": 123,
        "intensity": 40,
        "triggers": ["Friends"],
        "journal": "Great day!"
        # aiReflection is OMITTED
    }
    mood_resp = requests.post(f"{BASE_URL}moods/", json=mood_payload, headers={"Authorization": f"Bearer {token}"})
    print(f"Mood Create Status: {mood_resp.status_code}")
    if mood_resp.status_code == 201:
        created_mood = mood_resp.json()
        print(f"Auto-generated Reflection: {created_mood['aiReflection']}")
        assert "joyful" in created_mood['aiReflection'].lower()
        assert "moderate" in created_mood['aiReflection'].lower()
        print("Success!")

if __name__ == "__main__":
    test_reflection()
