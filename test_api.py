import requests
import json
import uuid
import time

BASE_URL = "http://127.0.0.1:8000/api/"

def test_onboarding_and_profile():
    print("\n--- Testing Onboarding & Profile ---")
    username = f"testuser_{int(time.time())}"
    payload = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "testpassword123"
    }
    
    # Register
    print(f"Registering user: {username}...")
    response = requests.post(f"{BASE_URL}users/", json=payload)
    print(f"Register Status: {response.status_code}")
    
    if response.status_code == 201:
        # Update Profile
        print(f"Updating profile for: {username}...")
        profile_payload = {
            "avatar_name": "calm_avatar",
            "language": "Hindi",
            "text_size": "Large"
        }
        response = requests.put(f"{BASE_URL}profile/{username}/", json=profile_payload)
        print(f"Update Profile Status: {response.status_code}")
        if response.status_code == 200:
            print("Profile updated successfully!")
            print(json.dumps(response.json(), indent=2))
    else:
        print(f"Registration failed: {response.text}")

def test_moods(username=None):
    print("\n--- Testing MoodEntry Endpoints ---")
    mood_id = str(uuid.uuid4())
    payload = {
        "id": mood_id,
        "timestampMillis": int(time.time() * 1000),
        "moodName": "Calm",
        "moodImageResId": 12345,
        "intensity": 80,
        "triggers": ["Music", "Nature"],
        "journal": "Feeling peaceful today.",
        "aiReflection": "Great to see you in a calm state."
    }
    if username:
        # Need user ID for foreign key if not null
        # In this simplistic backend, we might need to fetch the user ID first
        user_res = requests.get(f"{BASE_URL}users/")
        if user_res.status_code == 200:
            users = user_res.json()
            for u in users:
                if u['username'] == username:
                    payload['user'] = u['id']
                    break

    print(f"Creating mood entry with ID: {mood_id}...")
    response = requests.post(f"{BASE_URL}moods/", json=payload)
    print(f"POST Status: {response.status_code}")
    
    if response.status_code == 201:
        print("Mood entry created!")
    else:
        print(f"POST Failed: {response.text}")

def test_chat(username):
    print("\n--- Testing Chat API ---")
    user_res = requests.get(f"{BASE_URL}users/")
    user_id = None
    if user_res.status_code == 200:
        for u in user_res.json():
            if u['username'] == username:
                user_id = u['id']
                break
    
    if user_id:
        payload = {
            "user": user_id,
            "text": "I'm feeling a bit anxious today.",
            "mode": "CBT",
            "language": "English",
            "is_user": True
        }
        response = requests.post(f"{BASE_URL}chat/", json=payload)
        print(f"Chat POST Status: {response.status_code}")
        if response.status_code == 201:
            print("Chat message saved!")
            # Get history
            history_res = requests.get(f"{BASE_URL}chat/?username={username}")
            print(f"Chat History count: {len(history_res.json())}")

def test_activities(username):
    print("\n--- Testing Activities API ---")
    user_res = requests.get(f"{BASE_URL}users/")
    user_id = None
    if user_res.status_code == 200:
        for u in user_res.json():
            if u['username'] == username:
                user_id = u['id']
                break
    
    if user_id:
        payload = {
            "user": user_id,
            "activity_type": "Breathing",
            "duration_minutes": 5,
            "details": {"cycle": "4-7-8"}
        }
        response = requests.post(f"{BASE_URL}activities/", json=payload)
        print(f"Activity POST Status: {response.status_code}")

def test_dashboard(username):
    print("\n--- Testing Dashboard API ---")
    response = requests.get(f"{BASE_URL}dashboard/{username}/")
    print(f"Dashboard Status: {response.status_code}")
    if response.status_code == 200:
        print("Dashboard Data:")
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # Note: Ensure 'python manage.py runserver' is running
    try:
        # Create a fresh user for testing
        test_username = f"tester_{int(time.time())}"
        reg_payload = {"username": test_username, "email": f"{test_username}@test.com", "password": "pass"}
        requests.post(f"{BASE_URL}users/", json=reg_payload)
        
        test_onboarding_and_profile()
        test_moods(test_username)
        test_chat(test_username)
        test_activities(test_username)
        test_dashboard(test_username)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Run 'python manage.py runserver' first.")
