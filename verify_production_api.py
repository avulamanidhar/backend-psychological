import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/"

def test_production_flow():
    print("\n--- Testing Production-Ready Flow ---")
    username = f"prod_user_{int(time.time())}"
    email = f"{username}@example.com"
    password = "SecurePassword123!"
    
    # 1. Register User
    print(f"1. Registering user: {username}...")
    reg_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}users/", json=reg_payload)
    print(f"   Status: {response.status_code}")
    if response.status_code != 201:
        print(f"   Failed to register: {response.text}")
        return

    # 2. Login (Get JWT Token)
    print(f"2. Logging in to get JWT token...")
    login_payload = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}login/", json=login_payload)
    print(f"   Status: {response.status_code}")
    if response.status_code != 200:
        print(f"   Failed to login: {response.text}")
        return
    
    tokens = response.json()
    access_token = tokens['access']
    login_user = tokens.get('username')
    headers = {"Authorization": f"Bearer {access_token}"}
    print(f"   JWT Token obtained successfully for {login_user}!")

    # 3. Test Protected Endpoint (Profile)
    print(f"3. Testing protected profile endpoint...")
    response = requests.get(f"{BASE_URL}profile/{username}/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Profile retrieved: {response.json().get('username')}")
    else:
        print(f"   Failed to retrieve profile: {response.text}")

    # 4. Test Mood Entry with Auto AI Reflection
    print(f"4. Testing mood entry with auto-AI reflection...")
    mood_payload = {
        "id": f"mood_{int(time.time())}",
        "timestampMillis": int(time.time() * 1000),
        "moodName": "Anxious",
        "moodImageResId": 101,
        "intensity": 65,
        "triggers": ["Work", "Deadlines"],
        "journal": "Feeling overwhelmed with tasks."
    }
    response = requests.post(f"{BASE_URL}moods/", json=mood_payload, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        mood_data = response.json()
        mood_id = mood_data.get('id')
        print(f"   AI Reflection: {mood_data.get('aiReflection')}")
        
        # 11. Testing specific Mood Entry Detail endpoint
        print(f"11. Testing specific Mood Entry Detail endpoint for {mood_id}...")
        detail_resp = requests.get(f"{BASE_URL}moods/{mood_id}/", headers=headers)
        print(f"    Status: {detail_resp.status_code}")
        if detail_resp.status_code == 200:
            detail_data = detail_resp.json()
            print(f"    Mood Name: {detail_data.get('moodName')}")
            print(f"    Triggers: {detail_data.get('triggers')}")
            print(f"    Journal: {detail_data.get('journal')}")
        else:
            print(f"    Failed to fetch mood detail: {detail_resp.text}")
    else:
        print(f"   Failed to create mood: {response.text}")

    # 5. Testing chat with enhanced AI therapeutic response
    print("5. Testing chat with enhanced AI therapeutic response...")
    chat_payload = {
        "text": "I feel very anxious about my project.",
        "mode": "General",
        "language": "English"
    }
    chat_resp = requests.post(f"{BASE_URL}chat/", json=chat_payload, headers=headers)
    print(f"   Status: {chat_resp.status_code}")
    if chat_resp.status_code == 201:
        data = chat_resp.json()
        user_msg = data.get('user_message', {})
        ai_msg = data.get('ai_message', {})
        print(f"   User: {user_msg.get('text')}")
        print(f"   AI: {ai_msg.get('text')}")
    else:
        print(f"   Chat failed: {chat_resp.text}")

    # 6. Test Dashboard
    print(f"6. Testing dashboard summary...")
    response = requests.get(f"{BASE_URL}dashboard/{username}/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Greeting: {data.get('greeting')}")
        print(f"   Risk Level: {data.get('risk_level')}")
        print(f"   Recommendation: {data.get('recommended_activity')}")
        print(f"   Mental Health Score: {data.get('mental_health_score')}")
    else:
        print(f"   Failed to get dashboard: {response.text}")

    # 9. Testing Insight Trends with Summary
    print("9. Testing Insight Trends with Summary...")
    trends_resp = requests.get(f"{BASE_URL}insights/trends/{username}/", headers=headers)
    print(f"   Status: {trends_resp.status_code}")
    if trends_resp.status_code == 200:
        data = trends_resp.json()
        print(f"   Weekly Score: {data.get('weekly_summary_score')}")
        print(f"   Trend Text: {data.get('trend_text')}")
    else:
        print(f"   Failed to fetch trends: {trends_resp.text}")

    # 7. Test Swagger UI (Schema)
    print(f"7. Verifying schema endpoint availability...")
    response = requests.get(f"{BASE_URL}schema/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   Schema endpoint is up!")

    # 8. Testing Detected Patterns endpoint
    print("8. Testing Detected Patterns endpoint...")
    patterns_resp = requests.get(f"{BASE_URL}insights/patterns/{username}/", headers=headers)
    print(f"   Status: {patterns_resp.status_code}")
    if patterns_resp.status_code == 200:
        data = patterns_resp.json()
        if data:
            print(f"   Patterns count: {len(data)}")
            for p in data:
                print(f"   - {p['title']} ({p['confidence']}): {p['description'][:30]}...")
        else:
            print("   No patterns found.")
    else:
        print(f"   Failed to fetch patterns: {patterns_resp.text}")

    # 12. Testing Feedback submission
    print("12. Testing Feedback submission...")
    feedback_payload = {
        "subject": "App Experience",
        "message": "The AI reflections are very helpful!",
        "rating": 5
    }
    feed_resp = requests.post(f"{BASE_URL}feedback/", json=feedback_payload, headers=headers)
    print(f"    Status: {feed_resp.status_code}")
    if feed_resp.status_code == 201:
        print("    Feedback submitted successfully!")
    else:
        print(f"    Feedback submission failed: {feed_resp.text}")

    # 13. Testing Forgot Password (Username)
    print("13. Testing Forgot Password (Username)...")
    forgot_payload_user = {"username": username}
    forgot_resp_user = requests.post(f"{BASE_URL}forgot-password/", json=forgot_payload_user)
    print(f"    Status: {forgot_resp_user.status_code}")
    if forgot_resp_user.status_code == 200:
        print("    Reset message received via username!")

    # 14. Testing Forgot Password (Email)
    print("14. Testing Forgot Password (Email)...")
    forgot_payload_email = {"username": email}
    forgot_resp_email = requests.post(f"{BASE_URL}forgot-password/", json=forgot_payload_email)
    print(f"    Status: {forgot_resp_email.status_code}")
    if forgot_resp_email.status_code == 200:
        print("    Reset message received via email!")

    # 15. Testing Forgot Password (Invalid)
    print("15. Testing Forgot Password (Invalid)...")
    forgot_payload_inv = {"username": "non_existent_user_xyz"}
    forgot_resp_inv = requests.post(f"{BASE_URL}forgot-password/", json=forgot_payload_inv)
    print(f"    Status: {forgot_resp_inv.status_code}")
    if forgot_resp_inv.status_code == 404:
        print("    Correctly returned 404 for invalid user.")

    # 16. Testing Profile Update (Avatar & Age Range)
    print("16. Testing Profile Update (Avatar & Age Range)...")
    update_payload = {
        "avatar_name": "avatar_3",
        "age_range": "25 - 34",
        "goals": ["AI Support", "Meditation"],
        "language": "Spanish",
        "text_size": "Large",
        "high_contrast": True,
        "screen_reader": False
    }
    update_resp = requests.put(f"{BASE_URL}profile/{username}/", json=update_payload, headers=headers)
    print(f"    Status: {update_resp.status_code}")
    if update_resp.status_code == 200:
        data = update_resp.json()
        print(f"    Updated Avatar: {data.get('avatar_name')}")
        print(f"    Updated Age Range: {data.get('age_range')}")
        print(f"    Updated Goals: {data.get('goals')}")
        print(f"    Updated Language: {data.get('language')}")
        print(f"    Updated Text Size: {data.get('text_size')}")
        print(f"    Updated High Contrast: {data.get('high_contrast')}")
    else:
        print(f"    Profile update failed: {update_resp.text}")

    # 17. Testing FAQ endpoint
    print("17. Testing FAQ endpoint...")
    faq_resp = requests.get(f"{BASE_URL}faq/")
    print(f"    Status: {faq_resp.status_code}")
    if faq_resp.status_code == 200:
        data = faq_resp.json()
        print(f"    FAQs count: {len(data)}")
        for item in data[:3]:
            print(f"    - {item['question']}")
    else:
        print(f"    FAQ fetch failed: {faq_resp.text}")

    # 18. Testing How It Works endpoint
    print("18. Testing How It Works endpoint...")
    hiw_resp = requests.get(f"{BASE_URL}how-it-works/")
    print(f"    Status: {hiw_resp.status_code}")
    if hiw_resp.status_code == 200:
        data = hiw_resp.json()
        print(f"    Steps count: {len(data)}")
        for item in data[:3]:
            print(f"    - {item['title']}: {item['description'][:30]}...")
    else:
        print(f"    HIW fetch failed: {hiw_resp.text}")

    # 19. Testing System Status endpoint
    print("19. Testing System Status endpoint...")
    sys_resp = requests.get(f"{BASE_URL}system/status/")
    print(f"    Status: {sys_resp.status_code}")
    if sys_resp.status_code == 200:
        data = sys_resp.json()
        print(f"    Server Status: {data.get('status')}")
        print(f"    Server Time: {data.get('server_time')}")
        print(f"    Backend Version: {data.get('version')}")
    else:
        print(f"    Status fetch failed: {sys_resp.text}")

    # 20. Testing Key Indicators endpoint
    print(f"20. Testing Key Indicators for {username}...")
    ki_resp = requests.get(f"{BASE_URL}key-indicators/{username}/", headers=headers)
    print(f"    Status: {ki_resp.status_code}")
    if ki_resp.status_code == 200:
        data = ki_resp.json()
        for key in ['stress', 'anxiety', 'depression', 'stability']:
            metric = data.get(key, {})
            print(f"    - {key.capitalize()}: {metric.get('status')} ({metric.get('progress')}%)")
    else:
        print(f"    KI fetch failed: {ki_resp.text}")

    # 21. Testing Mood Trend Graph endpoint
    print(f"21. Testing Mood Trend Graph for {username}...")
    graph_resp = requests.get(f"{BASE_URL}insights/graph/{username}/", headers=headers)
    print(f"    Status: {graph_resp.status_code}")
    if graph_resp.status_code == 200:
        data = graph_resp.json()
        print(f"    Current Points: {data.get('current_points')[:3]}...")
        print(f"    Comparison Points: {data.get('comparison_points')[:3]}...")
    else:
        print(f"    Graph fetch failed: {graph_resp.text}")

    # 22. Testing App Config endpoint
    print(f"22. Testing App Config...")
    config_resp = requests.get(f"{BASE_URL}system/config/")
    print(f"    Status: {config_resp.status_code}")
    if config_resp.status_code == 200:
        configs = config_resp.json()
        print(f"    Configs count: {len(configs)}")
        for cfg in configs:
            print(f"    - {cfg.get('key')}: {cfg.get('value')}")
    else:
        print(f"    Config fetch failed: {config_resp.text}")

    # 23. Testing Activity Logging
    print(f"23. Testing Activity Logging...")
    activity_payload = {
        "activity_type": "Meditation",
        "duration_minutes": 10,
        "details": {"mode": "Calm"}
    }
    activity_resp = requests.post(f"{BASE_URL}activities/", json=activity_payload, headers=headers)
    print(f"    Status: {activity_resp.status_code}")
    if activity_resp.status_code == 201:
        print(f"    Activity logged successfully!")
    else:
        print(f"    Activity logging failed: {activity_resp.text}")

    # 24. Testing Mood Types
    print(f"24. Testing Mood Types...")
    mood_resp = requests.get(f"{BASE_URL}system/moods/", headers=headers)
    print(f"    Status: {mood_resp.status_code}")
    if mood_resp.status_code == 200:
        moods = mood_resp.json()
        print(f"    Mood types count: {len(moods)}")
        if moods:
            print(f"    Sample: {moods[0].get('name')} - {moods[0].get('color')}")
    else:
        print(f"    Mood types fetch failed: {mood_resp.text}")

    # 25. Testing Notifications
    print(f"25. Testing Notifications...")
    notif_resp = requests.get(f"{BASE_URL}notifications/", headers=headers)
    print(f"    Status: {notif_resp.status_code}")
    if notif_resp.status_code == 200:
        notifs = notif_resp.json()
        print(f"    Notifications count: {len(notifs)}")
        if notifs:
            notif_id = notifs[0]['id']
            print(f"    Sample: {notifs[0]['title']}")
            
            # Test Read
            print(f"    Marking notification {notif_id} as read...")
            read_resp = requests.patch(f"{BASE_URL}notifications/{notif_id}/", headers=headers)
            print(f"    Read Status: {read_resp.status_code}")
            
            # Test Delete
            print(f"    Deleting notification {notif_id}...")
            del_resp = requests.delete(f"{BASE_URL}notifications/{notif_id}/", headers=headers)
            print(f"    Delete Status: {del_resp.status_code}")
    else:
        print(f"    Notifications fetch failed: {notif_resp.text}")

    # 26. Testing Recommendations
    print(f"26. Testing Recommendations...")
    recs_resp = requests.get(f"{BASE_URL}recommendations/", headers=headers)
    print(f"    Status: {recs_resp.status_code}")
    if recs_resp.status_code == 200:
        recommendations = recs_resp.json()
        print(f"    Recommendations count: {len(recommendations)}")
        if recommendations:
            print(f"    Sample Recommendation: {recommendations[0]['title']}")
            print(f"    Type: {recommendations[0]['type']}")
            print(f"    Duration: {recommendations[0]['duration']}")
    else:
        print(f"    Recommendations fetch failed: {recs_resp.text}")

    # 27. Testing Privacy Policy & Consent registration
    print(f"27. Testing Privacy Policy & Consent registration...")
    # Fetch policy
    p_resp = requests.get(f"{BASE_URL}privacy-policy/")
    print(f"    Policy status: {p_resp.status_code}")
    if p_resp.status_code == 200:
        print(f"    Policy v: {p_resp.json().get('version')}")
    
    # Register with consent
    reg_name = f"consent_user_{int(time.time())}"
    reg_payload = {
        "username": reg_name,
        "password": "password123",
        "email": f"{reg_name}@privacy.com",
        "privacy_consent_accepted": True,
        "essential_data_processing": True,
        "anonymous_analytics": True,
        "privacy_policy_version": "1.0.0"
    }
    cre_resp = requests.post(f"{BASE_URL}users/", json=reg_payload)
    print(f"    Registration with consent Status: {cre_resp.status_code}")
    if cre_resp.status_code == 201:
        # Verify profile has the consent fields
        login_r = requests.post(f"{BASE_URL}login/", json={"username": reg_name, "password": "password123"})
        tok = login_r.json()['access']
        prof_r = requests.get(f"{BASE_URL}profile/{reg_name}/", headers={"Authorization": f"Bearer {tok}"})
        p_data = prof_r.json()
        print(f"    Consent Accepted in Profile: {p_data.get('privacy_consent_accepted')}")
        print(f"    Anonymous Analytics: {p_data.get('anonymous_analytics')}")
    else:
        print(f"    Registration failed: {cre_resp.text}")

    # 28. Testing Data Export & Delete
    print(f"28. Testing Data Export & Delete...")
    # Export
    ex_resp = requests.get(f"{BASE_URL}user/export/", headers={"Authorization": f"Bearer {tok}"})
    print(f"    Data Export Status: {ex_resp.status_code}")
    if ex_resp.status_code == 200:
        data = ex_resp.json()
        print(f"    Export Keys: {list(data.keys())}")
        print(f"    Moods Exported: {len(data.get('mood_history', []))}")
    
    # Delete
    del_resp = requests.delete(f"{BASE_URL}user/delete-data/", headers={"Authorization": f"Bearer {tok}"})
    print(f"    Data Delete Status: {del_resp.status_code}")
    
    # Verify deletion
    verify_resp = requests.get(f"{BASE_URL}user/export/", headers={"Authorization": f"Bearer {tok}"})
    v_data = verify_resp.json()
    print(f"    Moods after delete: {len(v_data.get('mood_history', []))}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    print("Ensure the Django server is running on http://127.0.0.1:8000")
    try:
        test_production_flow()
    except Exception as e:
        print(f"Error during verification: {e}")
