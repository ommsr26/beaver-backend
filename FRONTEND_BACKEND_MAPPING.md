# 🔌 Frontend-Backend API Mapping

Complete mapping of frontend components to backend endpoints.

## ✅ Phase 1: Quick Wins (Already Implemented)

### Navigation Component

| Frontend Need | Backend Endpoint | Status |
|--------------|------------------|--------|
| Account balance display | `GET /account/balance` | ✅ Ready |
| User avatar/menu | `GET /users/me` or `GET /auth/me` | ✅ Ready |
| "Sign In" button | `POST /auth/login` | ✅ Ready |
| "Get API Key" button | `POST /api-keys/generate` | ✅ Ready |

### Hero Component

| Frontend Need | Backend Endpoint | Status |
|--------------|------------------|--------|
| "100+ Models" stat | `GET /v1/models` (use `total` field) | ✅ Ready |
| "99.9% Uptime" stat | `GET /status/uptime` | ✅ Ready |
| "50ms Avg Latency" stat | `GET /status/latency` | ✅ Ready |

### Models Component

| Frontend Need | Backend Endpoint | Status |
|--------------|------------------|--------|
| Model list | `GET /v1/models` | ✅ Already Connected |
| Model cards | Returns id, display_name, provider, pricing | ✅ Working |

---

## 🚀 Phase 2: Core Features (Now Implemented)

### Authentication Flow

```typescript
// Register new user
POST /auth/register
Body: { email: string, password?: string, initial_balance?: number }
Response: { account: {...}, api_key: string, api_key_id: string }

// Login
POST /auth/login
Body: { email: string, password?: string }
Response: { account: {...}, api_key: string, api_key_id: string }

// Logout (stateless)
POST /auth/logout
Response: { message: "Logged out successfully" }

// Get current user
GET /auth/me
Headers: Authorization: Bearer {api_key}
Response: { id, email, balance, api_keys: [...] }
```

### API Key Management

```typescript
// List all API keys
GET /api-keys
Headers: Authorization: Bearer {api_key}
Response: { api_keys: [...], total: number }

// Create new API key
POST /api-keys
Headers: Authorization: Bearer {api_key}
Body: { name: string }
Response: { id, name, api_key: string, created_at }

// Generate API key (alias)
POST /api-keys/generate
Headers: Authorization: Bearer {api_key}
Response: { api_key: string, id, name, created_at }

// Delete API key
DELETE /api-keys/{key_id}
Headers: Authorization: Bearer {api_key}
Response: { message: "API key deleted successfully" }
```

### Chat Playground

```typescript
// Chat completion
POST /v1/models/{model_id}/chat
Headers: Authorization: Bearer {api_key}
Body: {
  messages: [{ role: "user" | "assistant" | "system", content: string }],
  temperature?: number,
  max_tokens?: number
}
Response: {
  id: string,
  model: string,
  choices: [{ message: { role, content } }],
  usage: { input_tokens, output_tokens }
}
```

---

## 📊 Phase 3: Dashboard Features (Now Implemented)

### Usage Analytics

```typescript
// Get usage statistics
GET /account/usage?days=30
Headers: Authorization: Bearer {api_key}
Response: {
  account_id: string,
  period_days: number,
  summary: {
    total_requests: number,
    total_input_tokens: number,
    total_output_tokens: number,
    total_tokens: number,
    total_cost: number
  },
  by_model: [
    {
      model_id: string,
      requests: number,
      input_tokens: number,
      output_tokens: number,
      cost: number
    }
  ]
}
```

### Billing History

```typescript
// Get billing history
GET /account/billing?limit=100
Headers: Authorization: Bearer {api_key}
Response: {
  account_id: string,
  transactions: [
    {
      id: string,
      amount: number,
      type: "topup" | "deduction",
      description: string,
      created_at: string
    }
  ],
  total: number
}

// Alternative endpoint (same data)
GET /account/transactions?limit=50
```

### User Settings

```typescript
// Get user info
GET /users/me
Headers: Authorization: Bearer {api_key}
Response: {
  id: string,
  email: string,
  balance: number,
  api_keys: [...],
  created_at: string
}

// Update user settings
PATCH /users/me
Headers: Authorization: Bearer {api_key}
Body: { email?: string }
Response: {
  id: string,
  email: string,
  balance: number,
  message: "User updated successfully"
}
```

---

## 🎯 Frontend Integration Guide

### 1. Update API Config

```typescript
// src/config/api.ts
export const API_BASE_URL = "http://localhost:8000";

// Helper functions
export const api = {
  // Auth
  register: (email: string, initialBalance = 0) =>
    fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, initial_balance: initialBalance })
    }),
  
  login: (email: string) =>
    fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    }),
  
  logout: () =>
    fetch(`${API_BASE_URL}/auth/logout`, { method: "POST" }),
  
  getCurrentUser: (apiKey: string) =>
    fetch(`${API_BASE_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  // API Keys
  listApiKeys: (apiKey: string) =>
    fetch(`${API_BASE_URL}/api-keys`, {
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  createApiKey: (apiKey: string, name: string) =>
    fetch(`${API_BASE_URL}/api-keys`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name })
    }),
  
  generateApiKey: (apiKey: string) =>
    fetch(`${API_BASE_URL}/api-keys/generate`, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  deleteApiKey: (apiKey: string, keyId: string) =>
    fetch(`${API_BASE_URL}/api-keys/${keyId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  // Account
  getBalance: (apiKey: string) =>
    fetch(`${API_BASE_URL}/account/balance`, {
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  getUsage: (apiKey: string, days = 30) =>
    fetch(`${API_BASE_URL}/account/usage?days=${days}`, {
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  getBilling: (apiKey: string, limit = 100) =>
    fetch(`${API_BASE_URL}/account/billing?limit=${limit}`, {
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  // Models
  getModels: (apiKey: string) =>
    fetch(`${API_BASE_URL}/v1/models`, {
      headers: { Authorization: `Bearer ${apiKey}` }
    }),
  
  // Chat
  chat: (apiKey: string, modelId: string, messages: any[], options = {}) =>
    fetch(`${API_BASE_URL}/v1/models/${modelId}/chat`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        messages,
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 512
      })
    }),
  
  // Status
  getUptime: () => fetch(`${API_BASE_URL}/status/uptime`),
  getLatency: () => fetch(`${API_BASE_URL}/status/latency`),
  
  // Users
  updateUser: (apiKey: string, data: { email?: string }) =>
    fetch(`${API_BASE_URL}/users/me`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
};
```

### 2. Update Navigation Component

```typescript
// Navigation.tsx
import { api } from '@/config/api';

// Get balance
const [balance, setBalance] = useState(0);
useEffect(() => {
  const apiKey = localStorage.getItem('api_key');
  if (apiKey) {
    api.getBalance(apiKey)
      .then(r => r.json())
      .then(data => setBalance(data.balance));
  }
}, []);

// Get user info
const [user, setUser] = useState(null);
useEffect(() => {
  const apiKey = localStorage.getItem('api_key');
  if (apiKey) {
    api.getCurrentUser(apiKey)
      .then(r => r.json())
      .then(setUser);
  }
}, []);
```

### 3. Update Hero Component

```typescript
// Hero.tsx
const [stats, setStats] = useState({
  modelCount: 100,
  uptime: "99.9%",
  latency: "50ms"
});

useEffect(() => {
  // Get model count
  const apiKey = localStorage.getItem('api_key');
  if (apiKey) {
    api.getModels(apiKey)
      .then(r => r.json())
      .then(data => setStats(prev => ({
        ...prev,
        modelCount: data.total
      })));
  }
  
  // Get uptime
  api.getUptime()
    .then(r => r.json())
    .then(data => setStats(prev => ({
      ...prev,
      uptime: data.uptime_percentage + "%"
    })));
  
  // Get latency
  api.getLatency()
    .then(r => r.json())
    .then(data => setStats(prev => ({
      ...prev,
      latency: data.average_latency_ms + "ms"
    })));
}, []);
```

---

## 📝 Summary

All frontend endpoints are now implemented:

✅ **Authentication**: Register, Login, Logout, Get Current User  
✅ **API Keys**: List, Create, Generate, Delete  
✅ **Account**: Balance, Usage Analytics, Billing History  
✅ **Models**: List (already working)  
✅ **Chat**: Completion (ready to use)  
✅ **Status**: Uptime, Latency  
✅ **Users**: Get/Update user settings  

Your frontend can now connect to all these endpoints!

