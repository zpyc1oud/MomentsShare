#!/usr/bin/env python
"""
Test script for AI model switching functionality.
Tests polish endpoint with different models.
"""
import os
import sys
import django
import requests
import json

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moments_share.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Configuration
API_BASE = "http://localhost:8000/api/v1"
MODELS_TO_TEST = [
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen3-VL-8B-Instruct",
    "zai-org/GLM-4.6V",
    "stepfun-ai/step3"
]

def get_auth_token():
    """Get or create a test user and return their JWT token."""
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            phone='13800138000'
        )
        print(f"✓ Created test user: {user.username}")

    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def test_model_polish(token, model_id):
    """Test polish endpoint with a specific model."""
    print(f"\n{'='*60}")
    print(f"Testing model: {model_id}")
    print(f"{'='*60}")

    url = f"{API_BASE}/ai/polish/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "text": "今天天气真好，想去公园散步",
        "model": model_id
    }

    print(f"Request: POST {url}")
    print(f"Model: {model_id}")
    print(f"Text: {data['text']}")

    try:
        # Use longer timeout for GLM models (they may take more time)
        timeout = 150 if 'GLM' in model_id else 60
        response = requests.post(url, headers=headers, data=data, timeout=timeout)
        print(f"\nResponse Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUCCESS!")
            print(f"  Polished Content: {result.get('polished_content', 'N/A')}")
            print(f"  Suggested Tags: {result.get('suggested_tags', [])}")
            return True
        else:
            print(f"✗ FAILED!")
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text}")
            return False

    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    """Run all model tests."""
    print("\n" + "="*60)
    print("AI Model Testing Script")
    print("="*60)

    # Get authentication token
    print("\n[1/2] Getting authentication token...")
    token = get_auth_token()
    print(f"✓ Token obtained: {token[:50]}...")

    # Test each model
    print("\n[2/2] Testing models...")
    results = {}

    for model_id in MODELS_TO_TEST:
        success = test_model_polish(token, model_id)
        results[model_id] = success

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    for model_id, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {model_id}")

    # Count results
    passed = sum(1 for s in results.values() if s)
    total = len(results)
    print(f"\nTotal: {passed}/{total} models passed")

    if passed == total:
        print("\n✓ All models working correctly!")
        return 0
    else:
        print(f"\n✗ {total - passed} model(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
