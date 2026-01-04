# 🦫 Beaver API Gateway - Complete Features & Functions

## 📋 Table of Contents
1. [Core Features](#core-features)
2. [API Endpoints](#api-endpoints)
3. [LLM Provider Integrations](#llm-provider-integrations)
4. [Supported Models](#supported-models)
5. [Security & Middleware](#security--middleware)
6. [Billing & Pricing](#billing--pricing)
7. [Database Models](#database-models)
8. [Frontend Integration](#frontend-integration)

---

## 🎯 Core Features

### 1. **Unified API Gateway**
- Single API key to access all LLM providers
- No need to manage multiple provider accounts
- Consistent API interface across all models

### 2. **Account Management System**
- User accounts with email-based registration
- Balance tracking and management
- Multiple API keys per account
- Account creation with initial balance

### 3. **Automatic Billing System**
- Real-time balance deduction
- Transaction logging (top-ups and deductions)
- Balance validation before requests
- Cost calculation with automatic markup

### 4. **Multi-Provider Support**
- **OpenAI** (GPT models)
- **Anthropic** (Claude models)
- **Google** (Gemini models)
- Easy to add more providers

### 5. **Usage Tracking & Analytics**
- Detailed usage logs per request
- Token usage tracking (input/output)
- Cost per request
- Model and provider tracking

### 6. **Rate Limiting**
- Per-API-key rate limits
- Configurable limits by plan (free/pro/enterprise)
- Prevents API abuse

### 7. **Usage Limits**
- Monthly request limits per plan
- Automatic limit enforcement
- Plan-based restrictions

### 8. **CORS Support**
- Pre-configured for Lovable frontend
- Supports multiple origins
- Development and production ready

---

## 🔌 API Endpoints

### **Health & Status**
- `GET /health` - Health check endpoint

### **Admin Endpoints** (Public - No Auth Required)
- `POST /admin/accounts` - Create new account
  - Body: `{email, initial_balance}`
  - Returns: account_id, email, balance
  
- `POST /admin/api-keys` - Create API key for account
  - Body: `{account_id, name}`
  - Returns: api_key, id, account_id
  
- `POST /admin/top-up` - Top up account balance
  - Body: `{account_id, amount}`
  - Returns: new_balance, transaction_id
  
- `GET /admin/accounts/{account_id}` - Get account details
  - Returns: account info + all API keys

### **User Endpoints** (Requires API Key)
- `GET /v1/models` - List all available models
  - Returns: models list with pricing info
  
- `POST /v1/models/{model_id}/chat` - Chat completion
  - Body: `{messages, temperature, max_tokens}`
  - Returns: chat response with usage stats
  - Automatically deducts balance
  
- `GET /account/balance` - Check account balance
  - Returns: account_id, email, balance, currency
  
- `GET /account/transactions` - Get transaction history
  - Query: `?limit=50`
  - Returns: list of transactions (top-ups & deductions)

### **Test Endpoints**
- `GET /protected` - Test authentication
  - Returns: API key info and account details

---

## 🤖 LLM Provider Integrations

### **1. OpenAI Provider** (`app/providers/openai_provider.py`)
- Full GPT model support
- Standard chat completions API
- Token usage tracking
- Error handling

### **2. Anthropic Provider** (`app/providers/anthropic_provider.py`)
- Claude model support
- Message format conversion
- System message handling
- Token usage tracking

### **3. Google Provider** (`app/providers/google_provider.py`)
- Gemini model support
- Content format conversion
- System instruction support
- Usage metadata tracking

---

## 📊 Supported Models (12 Total)

### **OpenAI Models (4)**
1. `gpt-4o` - Premium model ($2.50/$10.00 per 1M tokens)
2. `gpt-4o-mini` - Budget-friendly ($0.15/$0.60 per 1M tokens)
3. `gpt-4-turbo` - High-performance ($10.00/$30.00 per 1M tokens)
4. `gpt-3.5-turbo` - Cost-effective ($0.50/$1.50 per 1M tokens)

### **Anthropic Models (4)**
1. `claude-3-5-sonnet-20241022` - Latest Sonnet ($3.00/$15.00 per 1M tokens)
2. `claude-3-opus-20240229` - Most capable ($15.00/$75.00 per 1M tokens)
3. `claude-3-sonnet-20240229` - Balanced ($3.00/$15.00 per 1M tokens)
4. `claude-3-haiku-20240307` - Fast & affordable ($0.25/$1.25 per 1M tokens)

### **Google Models (4)**
1. `gemini-pro` - General purpose ($0.50/$1.50 per 1M tokens)
2. `gemini-pro-vision` - Vision-enabled ($0.50/$1.50 per 1M tokens)
3. `gemini-1.5-pro` - Advanced ($1.25/$5.00 per 1M tokens)
4. `gemini-1.5-flash` - Fast & efficient ($0.075/$0.30 per 1M tokens)

---

## 🔒 Security & Middleware

### **1. Authentication Middleware** (`app/middleware/auth.py`)
- API key validation
- Bearer token authentication
- Account balance checking
- Automatic account loading

### **2. Rate Limiting Middleware** (`app/middleware/rate_limit.py`)
- Per-API-key rate limits
- Plan-based limits:
  - Free: 60 requests/minute
  - Pro: 600 requests/minute
  - Enterprise: 5000 requests/minute

### **3. Usage Limit Middleware** (`app/middleware/usage_limit.py`)
- Monthly request limits:
  - Free: 10,000 requests/month
  - Pro: 200,000 requests/month
  - Enterprise: 5,000,000 requests/month

### **4. CORS Middleware**
- Pre-configured origins
- Credentials support
- All methods allowed
- Custom headers support

---

## 💰 Billing & Pricing

### **Pricing Categories & Markups**
- **ULTRA_BUDGET**: 10% markup
- **BUDGET**: 12.5% markup
- **MID_RANGE**: 15% markup
- **PREMIUM**: 5.5% markup
- **ULTRA_PREMIUM**: 3.5% markup

### **Cost Calculation**
- Automatic markup application
- Per-1M-token pricing
- Separate input/output pricing
- Real-time balance deduction
- Transaction logging

### **Transaction Types**
- **Top-up**: Adding balance to account
- **Deduction**: Automatic deduction on API usage

---

## 🗄️ Database Models

### **1. Account Model**
- `id` - Unique account identifier
- `email` - Unique email address
- `balance` - Current account balance (USD)
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp
- Relationship: One-to-many with APIKey

### **2. APIKey Model**
- `id` - Unique key identifier
- `key` - API key value (beaver_*)
- `name` - Human-readable key name
- `account_id` - Foreign key to Account
- `is_active` - Key status (active/inactive)
- `created_at` - Key creation timestamp
- Relationship: Many-to-one with Account

### **3. UsageLog Model**
- `id` - Unique log identifier
- `api_key_id` - API key used
- `account_id` - Account that made request
- `model_id` - Model used
- `provider` - Provider name
- `input_tokens` - Input tokens used
- `output_tokens` - Output tokens used
- `total_cost` - Cost of request
- `created_at` - Request timestamp

### **4. Transaction Model**
- `id` - Unique transaction identifier
- `account_id` - Account involved
- `amount` - Transaction amount (positive/negative)
- `transaction_type` - 'topup' or 'deduction'
- `description` - Transaction description
- `created_at` - Transaction timestamp

---

## 🎨 Frontend Integration

### **CORS Configuration**
- Production: `https://beaver-ai-hub.lovable.app`
- Development: `localhost:3000`, `localhost:5173`, `localhost:8080`

### **API Base URL**
- Development: `http://localhost:8000`
- Production: Your deployed backend URL

### **Authentication**
- Header: `Authorization: Bearer beaver_...`
- All protected endpoints require valid API key
- Balance checked on every request

### **Error Handling**
- Standard HTTP status codes
- Detailed error messages
- 401: Unauthorized (missing/invalid key)
- 402: Payment Required (insufficient balance)
- 403: Forbidden (disabled key)
- 404: Not Found (model/account not found)
- 429: Too Many Requests (rate limit)

---

## 🛠️ Technical Stack

### **Backend**
- **Framework**: FastAPI
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **ORM**: SQLAlchemy
- **Caching**: Redis (for rate limiting)
- **HTTP Client**: httpx (async)

### **Key Libraries**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `httpx` - HTTP client
- `redis` - Caching/rate limiting

---

## 📈 Usage Flow

1. **User Registration**
   - Create account via `/admin/accounts`
   - Get account_id

2. **API Key Creation**
   - Create API key via `/admin/api-keys`
   - Store API key securely

3. **Top Up Balance**
   - Add funds via `/admin/top-up`
   - Balance updated immediately

4. **Make API Calls**
   - Use API key in Authorization header
   - Call `/v1/models/{model_id}/chat`
   - Balance automatically deducted

5. **Monitor Usage**
   - Check balance via `/account/balance`
   - View transactions via `/account/transactions`
   - Usage logged automatically

---

## 🚀 Future Enhancements (Not Yet Implemented)

- [ ] Streaming support for chat completions
- [ ] WebSocket support
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Payment gateway integration
- [ ] Advanced analytics dashboard
- [ ] Model fine-tuning support
- [ ] Batch processing
- [ ] Webhook support

---

## 📝 Summary

**Beaver** is a fully functional unified API gateway with:
- ✅ 12 LLM models from 3 providers
- ✅ Complete account & billing system
- ✅ Rate limiting & usage tracking
- ✅ Frontend integration ready
- ✅ Production-ready architecture
- ✅ Comprehensive error handling
- ✅ Transaction logging
- ✅ Multi-provider support

The system is ready for production use and can be easily extended with additional features!


