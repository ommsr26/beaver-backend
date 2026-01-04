"""
Quick test script to verify the API is working and can connect to the frontend
Run this after starting the server: uvicorn app.main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_cors():
    """Test CORS headers"""
    print("🌐 Testing CORS configuration...")
    response = requests.options(
        f"{BASE_URL}/v1/models",
        headers={
            "Origin": "https://beaver-ai-hub.lovable.app",
            "Access-Control-Request-Method": "GET"
        }
    )
    print(f"Status: {response.status_code}")
    cors_headers = {
        k: v for k, v in response.headers.items() 
        if k.lower().startswith('access-control')
    }
    print(f"CORS Headers: {cors_headers}\n")
    return "access-control-allow-origin" in response.headers

def test_create_account():
    """Test account creation"""
    print("👤 Testing account creation...")
    data = {
        "email": f"test_{hash('test')}@example.com",
        "initial_balance": 10.0
    }
    response = requests.post(
        f"{BASE_URL}/admin/accounts",
        json=data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Account created: {result['account_id']}")
        print(f"Balance: ${result['balance']}\n")
        return result
    else:
        print(f"Error: {response.text}\n")
        return None

def test_create_api_key(account_id):
    """Test API key creation"""
    print("🔑 Testing API key creation...")
    data = {
        "account_id": account_id,
        "name": "Test API Key"
    }
    response = requests.post(
        f"{BASE_URL}/admin/api-keys",
        json=data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"API Key created: {result['api_key'][:20]}...")
        print(f"Key ID: {result['id']}\n")
        return result['api_key']
    else:
        print(f"Error: {response.text}\n")
        return None

def test_list_models(api_key):
    """Test listing models"""
    print("🤖 Testing list models endpoint...")
    response = requests.get(
        f"{BASE_URL}/v1/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Found {result['total']} models")
        print(f"Sample models: {[m['id'] for m in result['models'][:3]]}\n")
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

def test_chat(api_key, model_id="gpt-4o-mini"):
    """Test chat completion"""
    print(f"💬 Testing chat with {model_id}...")
    data = {
        "messages": [
            {"role": "user", "content": "Say hello in one word"}
        ],
        "temperature": 0.7,
        "max_tokens": 10
    }
    response = requests.post(
        f"{BASE_URL}/v1/models/{model_id}/chat",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['choices'][0]['message']['content']}")
        print(f"Tokens used: {result['usage']['input_tokens']} input + {result['usage']['output_tokens']} output\n")
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

def test_balance(api_key):
    """Test balance check"""
    print("💰 Testing balance check...")
    response = requests.get(
        f"{BASE_URL}/account/balance",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Account: {result['account_id']}")
        print(f"Balance: ${result['balance']}\n")
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

def main():
    print("=" * 60)
    print("🧪 Beaver API Connection Test")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    if not test_health():
        print("❌ Health check failed. Is the server running?")
        print("   Start with: uvicorn app.main:app --reload")
        return
    
    # Test 2: CORS
    if not test_cors():
        print("⚠️  CORS might not be configured correctly")
    else:
        print("✅ CORS is working")
    
    print("\n" + "=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)
    print()
    
    # Test 3: Create account
    account = test_create_account()
    if not account:
        print("❌ Account creation failed")
        return
    
    account_id = account['account_id']
    
    # Test 4: Create API key
    api_key = test_create_api_key(account_id)
    if not api_key:
        print("❌ API key creation failed")
        return
    
    # Test 5: List models
    if not test_list_models(api_key):
        print("❌ List models failed")
        return
    
    # Test 6: Check balance
    if not test_balance(api_key):
        print("❌ Balance check failed")
        return
    
    # Test 7: Chat (optional - requires OpenAI API key)
    print("💡 Chat test requires OPENAI_API_KEY in .env file")
    print("   Skipping chat test for now...\n")
    # Uncomment to test chat:
    # test_chat(api_key)
    
    print("=" * 60)
    print("✅ All basic tests passed!")
    print("=" * 60)
    print(f"\n📋 Your API Key for frontend: {api_key}")
    print(f"📋 Account ID: {account_id}")
    print("\n💡 Use this API key in your frontend to make requests!")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running:")
        print("   uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")


