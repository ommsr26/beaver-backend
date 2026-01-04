/**
 * API Configuration and Helper Functions
 * Connects to Beaver API Gateway backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Get API key from localStorage
const getApiKey = (): string => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('beaver_api_key') || '';
  }
  return '';
};

// Helper function to make authenticated requests
const authFetch = async (url: string, options: RequestInit = {}): Promise<Response> => {
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
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }
    return response.json();
  },

  login: async (email: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }
    return response.json();
  },

  logout: async () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('beaver_api_key');
    }
    return { message: 'Logged out' };
  },

  getCurrentUser: async () => {
    const response = await authFetch('/auth/me');
    if (!response.ok) {
      throw new Error('Failed to get user info');
    }
    return response.json();
  },

  // API Keys
  listApiKeys: async () => {
    const response = await authFetch('/api-keys');
    if (!response.ok) {
      throw new Error('Failed to list API keys');
    }
    return response.json();
  },

  createApiKey: async (name: string) => {
    const response = await authFetch('/api-keys', {
      method: 'POST',
      body: JSON.stringify({ name }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create API key');
    }
    return response.json();
  },

  generateApiKey: async () => {
    const response = await authFetch('/api-keys/generate', {
      method: 'POST',
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to generate API key');
    }
    return response.json();
  },

  deleteApiKey: async (keyId: string) => {
    const response = await authFetch(`/api-keys/${keyId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to delete API key');
    }
    return response.json();
  },

  // Account
  getBalance: async () => {
    const response = await authFetch('/account/balance');
    if (!response.ok) {
      throw new Error('Failed to get balance');
    }
    return response.json();
  },

  getUsage: async (days = 30) => {
    const response = await authFetch(`/account/usage?days=${days}`);
    if (!response.ok) {
      throw new Error('Failed to get usage');
    }
    return response.json();
  },

  getBilling: async (limit = 100) => {
    const response = await authFetch(`/account/billing?limit=${limit}`);
    if (!response.ok) {
      throw new Error('Failed to get billing');
    }
    return response.json();
  },

  getTransactions: async (limit = 50) => {
    const response = await authFetch(`/account/transactions?limit=${limit}`);
    if (!response.ok) {
      throw new Error('Failed to get transactions');
    }
    return response.json();
  },

  // Models
  getModels: async () => {
    const response = await authFetch('/v1/models');
    if (!response.ok) {
      throw new Error('Failed to get models');
    }
    return response.json();
  },

  // Chat
  chat: async (modelId: string, messages: any[], options = {}) => {
    const response = await authFetch(`/v1/models/${modelId}/chat`, {
      method: 'POST',
      body: JSON.stringify({
        messages,
        temperature: options.temperature || 0.7,
        max_tokens: options.max_tokens || 512,
      }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Chat request failed');
    }
    return response.json();
  },

  // Status
  getUptime: async () => {
    const response = await fetch(`${API_BASE_URL}/status/uptime`);
    if (!response.ok) {
      throw new Error('Failed to get uptime');
    }
    return response.json();
  },

  getLatency: async () => {
    const response = await fetch(`${API_BASE_URL}/status/latency`);
    if (!response.ok) {
      throw new Error('Failed to get latency');
    }
    return response.json();
  },

  // Users
  updateUser: async (data: { email?: string }) => {
    const response = await authFetch('/users/me', {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update user');
    }
    return response.json();
  },
};

