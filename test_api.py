import requests
import json
import uuid
import time

BASE_URL = "http://127.0.0.1:8000/api/"

def test_moods():
    print("--- Testing MoodEntry Endpoints ---")
    
    # 1. POST (Create)
    mood_id = str(uuid.uuid4())
    payload = {
        "id": mood_id,
        "timestampMillis": int(time.time() * 1000),
        "moodName": "Tested",
        "moodImageResId": 2131230870,
        "intensity": 75,
        "triggers": ["Testing", "API"],
        "journal": "This is a test entry created by the test script.",
        "aiReflection": "The API seems to be working well."
    }
    
    print(f"Creating mood entry with ID: {mood_id}...")
    response = requests.post(f"{BASE_URL}moods/", json=payload)
    print(f"POST Status: {response.status_code}")
    if response.status_code == 201:
        print("POST Success!")
    else:
        print(f"POST Failed: {response.text}")
        return

    # 2. GET (List)
    print("Listing all mood entries...")
    response = requests.get(f"{BASE_URL}moods/")
    print(f"GET List Status: {response.status_code}")
    if response.status_code == 200:
        entries = response.json()
        print(f"Found {len(entries)} entries.")
    else:
        print(f"GET List Failed: {response.text}")

    # 3. GET (Detail)
    print(f"Retrieving mood entry with ID: {mood_id}...")
    response = requests.get(f"{BASE_URL}moods/{mood_id}/")
    print(f"GET Detail Status: {response.status_code}")
    if response.status_code == 200:
        print("GET Detail Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"GET Detail Failed: {response.text}")

def test_users():
    print("\n--- Testing User Endpoints ---")
    # 1. GET (List)
    print("Listing all users...")
    response = requests.get(f"{BASE_URL}users/")
    print(f"GET Users Status: {response.status_code}")
    if response.status_code == 200:
        users = response.json()
        print(f"Found {len(users)} users.")
        if users:
            print(json.dumps(users[0], indent=2))
    else:
        print(f"GET Users Failed: {response.text}")

if __name__ == "__main__":
    try:
        test_moods()
        test_users()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure 'python manage.py runserver' is running in the 'Backend psychological' folder.")
