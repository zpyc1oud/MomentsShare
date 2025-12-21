import requests
import time

BASE_URL = "http://localhost:8000/api/v1"
AUTH_URL = f"{BASE_URL}/auth/login/"
POLISH_URL = f"{BASE_URL}/ai/polish/"
TAGS_URL = f"{BASE_URL}/ai/recommend-tags/"

# Test User Credentials (ensure this user exists or register one)
PHONE = "13800138000"
PASSWORD = "password123"

def get_token():
    """Login and get access token."""
    print(f"Logging in with {PHONE}...")
    try:
        response = requests.post(AUTH_URL, json={
            "phone": PHONE,
            "password": PASSWORD
        })
        if response.status_code == 200:
            token = response.json().get("access")
            print("Login successful.")
            return token
        else:
            print(f"Login failed: {response.text}")
            # Try registering if login fails
            register_url = f"{BASE_URL}/auth/register/"
            print("Trying to register...")
            reg_response = requests.post(register_url, json={
                "phone": PHONE,
                "password": PASSWORD,
                "username": "testuser_ai",
                "nickname": "AI Tester"
            })
            if reg_response.status_code == 201:
                print("Registration successful. Logging in again...")
                return get_token() # Recursion once
            else:
                print(f"Registration failed: {reg_response.text}")
                return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def test_polish(token, model=None):
    """Test text polishing."""
    headers = {"Authorization": f"Bearer {token}"}
    data = {"text": "今天天气不错，我去公园玩了一圈，开心。"}
    if model:
        data["model"] = model
        print(f"\n--- Testing Polish with Model: {model} ---")
    else:
        print(f"\n--- Testing Polish with Default Model ---")

    try:
        start_time = time.time()
        response = requests.post(POLISH_URL, json=data, headers=headers)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: Success (took {duration:.2f}s)")
            print(f"Polished: {result.get('polished_content')}")
            print(f"Tags: {result.get('suggested_tags')}")
        else:
            print(f"Status: Failed ({response.status_code})")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_tags(token):
    """Test tag recommendation."""
    print(f"\n--- Testing Tag Recommendation (Default Model) ---")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"text": "新开的咖啡店味道很赞，拿铁拉花很漂亮。"}
    
    try:
        start_time = time.time()
        response = requests.post(TAGS_URL, json=data, headers=headers)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: Success (took {duration:.2f}s)")
            print(f"Tags: {result.get('tags')}")
        else:
            print(f"Status: Failed ({response.status_code})")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Waiting for services to be fully ready (5s)...")
    time.sleep(5)
    
    token = get_token()
    if token:
        # 1. Test Polish with Default Model (Qwen-7B from .env)
        test_polish(token)
        
        # 2. Test Polish with Explicit Model (DeepSeek-V3)
        # Note: This depends on if the API Key has access to DeepSeek-V3 on SiliconFlow
        test_polish(token, model="deepseek-ai/DeepSeek-V3")
        
        # 3. Test Tag Recommendation
        test_tags(token)
    else:
        print("Skipping tests due to authentication failure.")
