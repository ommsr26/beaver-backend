# Frontend Integration Guide

This guide explains how to connect your Lovable frontend (https://beaver-ai-hub.lovable.app) to the Beaver API backend.

## Backend Configuration

The backend is now configured to accept requests from your frontend. CORS has been enabled with the following origins:

- `https://beaver-ai-hub.lovable.app` (Production frontend)
- `http://localhost:3000` (Local development)
- `http://localhost:5173` (Vite dev server)
- `http://localhost:8080` (Alternative local port)

## API Base URL

Set your frontend's API base URL to point to your backend server:

**Development:**
```
http://localhost:8000
```

**Production:**
```
https://your-backend-domain.com
```

## API Endpoints for Frontend

### 1. Create Account (Public - No Auth Required)
```javascript
POST /admin/accounts
Content-Type: application/json

{
  "email": "user@example.com",
  "initial_balance": 10.0
}

Response:
{
  "account_id": "acc_...",
  "email": "user@example.com",
  "balance": 10.0,
  "created_at": "2024-01-01T00:00:00"
}
```

### 2. Create API Key (Public - No Auth Required)
```javascript
POST /admin/api-keys
Content-Type: application/json

{
  "account_id": "acc_...",
  "name": "My API Key"
}

Response:
{
  "id": "...",
  "name": "My API Key",
  "api_key": "beaver_...",
  "account_id": "acc_...",
  "created_at": "2024-01-01T00:00:00"
}
```

### 3. Top Up Account (Public - No Auth Required)
```javascript
POST /admin/top-up
Content-Type: application/json

{
  "account_id": "acc_...",
  "amount": 50.0
}

Response:
{
  "account_id": "acc_...",
  "new_balance": 60.0,
  "amount_added": 50.0,
  "transaction_id": "txn_..."
}
```

### 4. List Available Models (Requires Auth)
```javascript
GET /v1/models
Authorization: Bearer beaver_your_api_key

Response:
{
  "models": [
    {
      "id": "gpt-4o-mini",
      "provider": "openai",
      "category": "BUDGET",
      "pricing": {
        "input_price_per_1m": 0.15,
        "output_price_per_1m": 0.6
      }
    },
    ...
  ],
  "total": 12
}
```

### 5. Chat Completion (Requires Auth)
```javascript
POST /v1/models/{model_id}/chat
Authorization: Bearer beaver_your_api_key
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 512
}

Response:
{
  "id": "beaver-...",
  "model": "gpt-4o-mini",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      }
    }
  ],
  "usage": {
    "input_tokens": 5,
    "output_tokens": 10
  }
}
```

### 6. Check Balance (Requires Auth)
```javascript
GET /account/balance
Authorization: Bearer beaver_your_api_key

Response:
{
  "account_id": "acc_...",
  "email": "user@example.com",
  "balance": 9.95,
  "currency": "USD"
}
```

### 7. Get Transactions (Requires Auth)
```javascript
GET /account/transactions?limit=50
Authorization: Bearer beaver_your_api_key

Response:
{
  "account_id": "acc_...",
  "transactions": [
    {
      "id": "txn_...",
      "amount": -0.05,
      "type": "deduction",
      "description": "API usage: gpt-4o-mini (5 input + 10 output tokens)",
      "created_at": "2024-01-01T00:00:00"
    },
    ...
  ]
}
```

## Frontend Implementation Example

### Using Fetch API

```javascript
// Store API key in localStorage or state management
const API_KEY = localStorage.getItem('beaver_api_key');
const API_BASE_URL = 'http://localhost:8000'; // or your production URL

// Make a chat request
async function sendMessage(modelId, messages) {
  const response = await fetch(`${API_BASE_URL}/v1/models/${modelId}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      messages,
      temperature: 0.7,
      max_tokens: 512
    })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }
  
  return await response.json();
}

// Get account balance
async function getBalance() {
  const response = await fetch(`${API_BASE_URL}/account/balance`, {
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
    }
  });
  
  return await response.json();
}

// List available models
async function getModels() {
  const response = await fetch(`${API_BASE_URL}/v1/models`, {
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
    }
  });
  
  return await response.json();
}
```

### Using Axios

```javascript
import axios from 'axios';

const API_KEY = localStorage.getItem('beaver_api_key');
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
  }
});

// Chat completion
export const sendMessage = async (modelId, messages) => {
  const response = await api.post(`/v1/models/${modelId}/chat`, {
    messages,
    temperature: 0.7,
    max_tokens: 512
  });
  return response.data;
};

// Get balance
export const getBalance = async () => {
  const response = await api.get('/account/balance');
  return response.data;
};

// List models
export const getModels = async () => {
  const response = await api.get('/v1/models');
  return response.data;
};
```

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (missing/invalid API key)
- `402` - Payment Required (insufficient balance)
- `403` - Forbidden (disabled API key)
- `404` - Not Found (model not found)
- `429` - Too Many Requests (rate limit exceeded)

Example error response:
```json
{
  "detail": "Insufficient balance. Required: $0.05, Available: $0.02"
}
```

## Testing the Connection

1. **Start your backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Test from browser console:**
   ```javascript
   // First create an account and API key using the admin endpoints
   // Then test with:
   fetch('http://localhost:8000/v1/models', {
     headers: {
       'Authorization': 'Bearer beaver_your_api_key_here'
     }
   })
   .then(r => r.json())
   .then(console.log);
   ```

## Environment Variables

Make sure your backend `.env` file includes:

```env
FRONTEND_URL=https://beaver-ai-hub.lovable.app
CORS_ORIGINS=["https://beaver-ai-hub.lovable.app","http://localhost:3000"]
```

Or the backend will use the default CORS origins configured in `app/config.py`.

