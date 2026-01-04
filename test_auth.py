"""
Quick test script for password authentication
Tests registration, login, and token usage
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    print("=" * 60)
    print("🧪 Testing Registration")
    print("=" * 60)
    
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test_auth@example.com",
        "password": "Test1234",
        "initial_balance": 10.0
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration successful!")
            print(f"Account ID: {result['account']['id']}")
            print(f"Email: {result['account']['email']}")
            print(f"Balance: ${result['account']['balance']}")
            print(f"API Key: {result['api_key'][:30]}...")
            return result
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_login(email, password):
    """Test user login"""
    print("\n" + "=" * 60)
    print("🧪 Testing Login")
    print("=" * 60)
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"Access Token: {result['access_token'][:50]}...")
            print(f"Refresh Token: {result['refresh_token'][:50]}...")
            print(f"Token Type: {result['token_type']}")
            print(f"Expires In: {result['expires_in']} seconds")
            return result
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_get_me(access_token):
    """Test getting current user with JWT token"""
    print("\n" + "=" * 60)
    print("🧪 Testing GET /auth/me with JWT")
    print("=" * 60)
    
    url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Get user info successful!")
            print(f"ID: {result['id']}")
            print(f"Email: {result['email']}")
            print(f"Balance: ${result['balance']}")
            print(f"Email Verified: {result['email_verified']}")
            print(f"API Keys: {len(result['api_keys'])}")
            return True
        else:
            print(f"❌ Get user info failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_refresh_token(refresh_token):
    """Test token refresh"""
    print("\n" + "=" * 60)
    print("🧪 Testing Token Refresh")
    print("=" * 60)
    
    url = f"{BASE_URL}/auth/refresh"
    data = {
        "refresh_token": refresh_token
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Token refresh successful!")
            print(f"New Access Token: {result['access_token'][:50]}...")
            print(f"New Refresh Token: {result['refresh_token'][:50]}...")
            return result
        else:
            print(f"❌ Token refresh failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    print("\n" + "=" * 60)
    print("🦫 Beaver Authentication Test Suite")
    print("=" * 60)
    print("\n⚠️  Make sure the server is running: uvicorn app.main:app --reload")
    print("⚠️  Make sure JWT_SECRET is set in .env file")
    print()
    
    # Test registration
    reg_result = test_registration()
    if not reg_result:
        print("\n❌ Registration failed. Cannot continue tests.")
        sys.exit(1)
    
    email = reg_result['account']['email']
    password = "Test1234"
    
    # Test login
    login_result = test_login(email, password)
    if not login_result:
        print("\n❌ Login failed. Cannot continue tests.")
        sys.exit(1)
    
    access_token = login_result['access_token']
    refresh_token = login_result['refresh_token']
    
    # Test get current user
    test_get_me(access_token)
    
    # Test refresh token
    refresh_result = test_refresh_token(refresh_token)
    if refresh_result:
        # Test with new token
        test_get_me(refresh_result['access_token'])
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

