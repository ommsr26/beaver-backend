# 🎨 Lovable Frontend Integration Guide

## Quick Setup Commands for Lovable

### 1. Update API Configuration

In your Lovable project, update `src/config/api.ts` (or create it):

```typescript
// src/config/api.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Get API key from localStorage
const getApiKey = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('beaver_api_key') || '';
  }
  return '';
};

// Helper function to make authenticated requests
const authFetch = async (url: string, options: RequestInit = {}) => {
  const apiKey = getApiKey();
  return fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
      ...options.headers,
    },
  });
};

export const api = {
  // Authentication
  register: async (email: string, initialBalance = 0) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, initial_balance: initialBalance }),
    });
    return response.json();
  },

  login: async (email: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    return response.json();
  },

  logout: async () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('beaver_api_key');
    }
    return { message: 'Logged out' };
  },

  getCurrentUser: async () => {
    return authFetch('/auth/me').then(r => r.json());
  },

  // API Keys
  listApiKeys: async () => {
    return authFetch('/api-keys').then(r => r.json());
  },

  createApiKey: async (name: string) => {
    return authFetch('/api-keys', {
      method: 'POST',
      body: JSON.stringify({ name }),
    }).then(r => r.json());
  },

  generateApiKey: async () => {
    return authFetch('/api-keys/generate', {
      method: 'POST',
    }).then(r => r.json());
  },

  deleteApiKey: async (keyId: string) => {
    return authFetch(`/api-keys/${keyId}`, {
      method: 'DELETE',
    }).then(r => r.json());
  },

  // Account
  getBalance: async () => {
    return authFetch('/account/balance').then(r => r.json());
  },

  getUsage: async (days = 30) => {
    return authFetch(`/account/usage?days=${days}`).then(r => r.json());
  },

  getBilling: async (limit = 100) => {
    return authFetch(`/account/billing?limit=${limit}`).then(r => r.json());
  },

  getTransactions: async (limit = 50) => {
    return authFetch(`/account/transactions?limit=${limit}`).then(r => r.json());
  },

  // Models
  getModels: async () => {
    return authFetch('/v1/models').then(r => r.json());
  },

  // Chat
  chat: async (modelId: string, messages: any[], options = {}) => {
    return authFetch(`/v1/models/${modelId}/chat`, {
      method: 'POST',
      body: JSON.stringify({
        messages,
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 512,
      }),
    }).then(r => r.json());
  },

  // Status
  getUptime: async () => {
    return fetch(`${API_BASE_URL}/status/uptime`).then(r => r.json());
  },

  getLatency: async () => {
    return fetch(`${API_BASE_URL}/status/latency`).then(r => r.json());
  },

  // Users
  updateUser: async (data: { email?: string }) => {
    return authFetch('/users/me', {
      method: 'PATCH',
      body: JSON.stringify(data),
    }).then(r => r.json());
  },
};
```

### 2. Environment Variables

Create `.env.local` in your Lovable project root:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set:
```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

### 3. Update Navigation Component

**Command for Lovable:**
```
Update Navigation.tsx to fetch and display account balance and user info using api.getBalance() and api.getCurrentUser()
```

**Code to add:**

```typescript
// Navigation.tsx
import { useState, useEffect } from 'react';
import { api } from '@/config/api';

export default function Navigation() {
  const [balance, setBalance] = useState(0);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiKey = localStorage.getItem('beaver_api_key');
    if (apiKey) {
      Promise.all([
        api.getBalance().then(data => setBalance(data.balance)),
        api.getCurrentUser().then(data => setUser(data))
      ]).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const handleSignIn = async () => {
    // Navigate to login page or show login modal
    window.location.href = '/auth/login';
  };

  const handleGetApiKey = async () => {
    // Navigate to API key generation page
    window.location.href = '/dashboard/keys';
  };

  return (
    <nav>
      {/* Your existing nav structure */}
      
      {/* Add balance display */}
      {user && (
        <div className="balance">
          Balance: ${balance.toFixed(2)}
        </div>
      )}
      
      {/* Add user avatar/menu */}
      {user ? (
        <div className="user-menu">
          <span>{user.email}</span>
          <span>${balance.toFixed(2)}</span>
        </div>
      ) : (
        <>
          <button onClick={handleSignIn}>Sign In</button>
          <button onClick={handleGetApiKey}>Get API Key</button>
        </>
      )}
    </nav>
  );
}
```

### 4. Update Hero Component

**Command for Lovable:**
```
Update Hero.tsx to fetch dynamic stats: model count from api.getModels(), uptime from api.getUptime(), and latency from api.getLatency()
```

**Code to add:**

```typescript
// Hero.tsx
import { useState, useEffect } from 'react';
import { api } from '@/config/api';

export default function Hero() {
  const [stats, setStats] = useState({
    modelCount: 100,
    uptime: '99.9%',
    latency: '50ms'
  });

  useEffect(() => {
    // Get model count
    const apiKey = localStorage.getItem('beaver_api_key');
    if (apiKey) {
      api.getModels()
        .then(data => setStats(prev => ({ ...prev, modelCount: data.total })))
        .catch(() => {});
    }

    // Get uptime (public endpoint)
    api.getUptime()
      .then(data => setStats(prev => ({ ...prev, uptime: `${data.uptime_percentage}%` })))
      .catch(() => {});

    // Get latency (public endpoint)
    api.getLatency()
      .then(data => setStats(prev => ({ ...prev, latency: `${data.average_latency_ms}ms` })))
      .catch(() => {});
  }, []);

  return (
    <div className="hero">
      {/* Your existing hero content */}
      
      <div className="stats">
        <div className="stat">
          <span className="stat-value">{stats.modelCount}+</span>
          <span className="stat-label">Models</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stats.uptime}</span>
          <span className="stat-label">Uptime</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stats.latency}</span>
          <span className="stat-label">Avg Latency</span>
        </div>
      </div>
    </div>
  );
}
```

### 5. Create Authentication Pages

**Command for Lovable:**
```
Create /auth/login page with form that calls api.login(email) and stores the returned api_key in localStorage as 'beaver_api_key', then redirects to dashboard
```

**Login Page Code:**

```typescript
// app/auth/login/page.tsx (or pages/auth/login.tsx)
'use client';
import { useState } from 'react';
import { api } from '@/config/api';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await api.login(email);
      if (data.api_key) {
        localStorage.setItem('beaver_api_key', data.api_key);
        router.push('/dashboard');
      } else {
        setError('Login failed');
      }
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Sign In'}
        </button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}
```

**Register Page Code:**

```typescript
// app/auth/register/page.tsx
'use client';
import { useState } from 'react';
import { api } from '@/config/api';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await api.register(email, 0);
      if (data.api_key) {
        localStorage.setItem('beaver_api_key', data.api_key);
        router.push('/dashboard');
      } else {
        setError('Registration failed');
      }
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page">
      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Sign Up'}
        </button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}
```

### 6. Create API Key Management Page

**Command for Lovable:**
```
Create /dashboard/keys page that lists API keys using api.listApiKeys(), allows creating new keys with api.createApiKey(name), and deleting keys with api.deleteApiKey(keyId)
```

**API Keys Page Code:**

```typescript
// app/dashboard/keys/page.tsx
'use client';
import { useState, useEffect } from 'react';
import { api } from '@/config/api';

export default function ApiKeysPage() {
  const [keys, setKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newKeyName, setNewKeyName] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    loadKeys();
  }, []);

  const loadKeys = async () => {
    try {
      const data = await api.listApiKeys();
      setKeys(data.api_keys || []);
    } catch (err) {
      console.error('Failed to load API keys', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateKey = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    try {
      const data = await api.createApiKey(newKeyName || 'New Key');
      await loadKeys();
      setNewKeyName('');
      // Show the new API key to user (they should copy it)
      alert(`New API Key: ${data.api_key}\n\nCopy this key - it won't be shown again!`);
    } catch (err: any) {
      alert(err.message || 'Failed to create API key');
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteKey = async (keyId: string) => {
    if (!confirm('Are you sure you want to delete this API key?')) return;
    
    try {
      await api.deleteApiKey(keyId);
      await loadKeys();
    } catch (err: any) {
      alert(err.message || 'Failed to delete API key');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="api-keys-page">
      <h1>API Keys</h1>
      
      <form onSubmit={handleCreateKey}>
        <input
          type="text"
          placeholder="Key name"
          value={newKeyName}
          onChange={(e) => setNewKeyName(e.target.value)}
        />
        <button type="submit" disabled={creating}>
          {creating ? 'Creating...' : 'Create API Key'}
        </button>
      </form>

      <div className="keys-list">
        {keys.map((key: any) => (
          <div key={key.id} className="key-item">
            <div>
              <strong>{key.name}</strong>
              <span>{key.key_preview}</span>
              <span>{key.is_active ? 'Active' : 'Inactive'}</span>
            </div>
            <button onClick={() => handleDeleteKey(key.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 7. Create Chat Playground

**Command for Lovable:**
```
Create /playground page with model selector and chat interface that uses api.chat(modelId, messages) to send messages and display responses
```

**Chat Playground Code:**

```typescript
// app/playground/page.tsx
'use client';
import { useState, useEffect } from 'react';
import { api } from '@/config/api';

export default function PlaygroundPage() {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    try {
      const data = await api.getModels();
      setModels(data.models || []);
      if (data.models?.length > 0) {
        setSelectedModel(data.models[0].id);
      }
    } catch (err) {
      console.error('Failed to load models', err);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !selectedModel) return;

    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await api.chat(selectedModel, newMessages);
      const assistantMessage = response.choices[0].message;
      setMessages([...newMessages, assistantMessage]);
    } catch (err: any) {
      alert(err.message || 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="playground">
      <div className="model-selector">
        <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
          {models.map((model: any) => (
            <option key={model.id} value={model.id}>
              {model.display_name} ({model.provider})
            </option>
          ))}
        </select>
      </div>

      <div className="chat-messages">
        {messages.map((msg: any, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
        {loading && <div>Thinking...</div>}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
        />
        <button onClick={handleSend} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}
```

---

## 🚀 Quick Setup Checklist

1. ✅ **Create/Update `src/config/api.ts`** with all API functions
2. ✅ **Set environment variable** `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. ✅ **Update Navigation.tsx** to show balance and user info
4. ✅ **Update Hero.tsx** to show dynamic stats
5. ✅ **Create `/auth/login` page** for user login
6. ✅ **Create `/auth/register` page** for user registration
7. ✅ **Create `/dashboard/keys` page** for API key management
8. ✅ **Create `/playground` page** for chat testing

---

## 🔧 Backend Setup

Make sure your backend is running:

```bash
# Start the backend server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

---

## 📝 Testing

1. **Test Registration:**
   - Go to `/auth/register`
   - Enter email
   - Should get API key and redirect to dashboard

2. **Test Login:**
   - Go to `/auth/login`
   - Enter registered email
   - Should get API key and redirect

3. **Test API Keys:**
   - Go to `/dashboard/keys`
   - Create new key
   - Verify it appears in list

4. **Test Chat:**
   - Go to `/playground`
   - Select model
   - Send message
   - Should get response

---

## 🎯 Summary

**For Lovable, use these commands:**

1. "Create API configuration file at `src/config/api.ts` with all backend endpoints"
2. "Update Navigation component to fetch and display account balance using `api.getBalance()`"
3. "Update Hero component to fetch dynamic stats from backend API"
4. "Create login page at `/auth/login` that calls `api.login()` and stores API key"
5. "Create register page at `/auth/register` that calls `api.register()`"
6. "Create API keys management page at `/dashboard/keys`"
7. "Create chat playground at `/playground` using `api.chat()`"

All the code examples above are ready to copy-paste into Lovable!

