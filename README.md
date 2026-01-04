# 🦫 Beaver - Unified API Gateway for LLMs

Beaver is a unified API gateway that allows you to access any AI model using a single API key. No need to manage multiple provider accounts or buy tokens from different providers. Simply top up your Beaver account and get access to all models with one key!

## ✨ Features

- **Unified API**: Access multiple LLM providers (OpenAI, Anthropic, Google) with one API key
- **Account Management**: Top up your account balance and use it across all models
- **Automatic Billing**: Balance is automatically deducted based on usage
- **Multiple Models**: Support for GPT-4, Claude, Gemini, and more
- **Rate Limiting**: Built-in rate limiting to prevent abuse
- **Usage Tracking**: Comprehensive usage logs and transaction history
- **Cost Transparency**: Clear pricing with automatic markup calculation
- **Frontend Ready**: CORS enabled for frontend integration (Lovable, React, Vue, etc.)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis (for rate limiting)
- SQLite (default database, can be changed to PostgreSQL)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Beaver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```env
APP_NAME=beaver
ENV=dev
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key  # Optional
GOOGLE_API_KEY=your_google_api_key  # Optional
```

4. Set up the database:
```bash
# For new installations (creates tables)
python init_db.py

# OR use Alembic migrations (recommended for production)
pip install -r requirements.txt  # Installs alembic
python -m alembic upgrade head   # Applies all migrations
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Integration

The backend is configured to work with your Lovable frontend at `https://beaver-ai-hub.lovable.app`. CORS is enabled by default.

For detailed frontend integration instructions, see [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md)

### Quick Start Guide

1. **Create your first account:**
```bash
curl -X POST "http://localhost:8000/admin/accounts" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "initial_balance": 10.0
  }'
```

2. **Create an API key for your account:**
```bash
curl -X POST "http://localhost:8000/admin/api-keys" \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "acc_...",
    "name": "My First Key"
  }'
```

3. **Make your first API call:**
```bash
curl -X POST "http://localhost:8000/v1/models/gpt-4o-mini/chat" \
  -H "Authorization: Bearer beaver_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, world!"}
    ]
  }'
```

## 📚 API Documentation

### Authentication

All API requests (except health checks and admin endpoints) require authentication using a Bearer token:

```bash
Authorization: Bearer beaver_your_api_key_here
```

### Admin Endpoints

#### Create Account
```bash
POST /admin/accounts
Content-Type: application/json

{
  "email": "user@example.com",
  "initial_balance": 10.0
}
```

#### Create API Key
```bash
POST /admin/api-keys
Content-Type: application/json

{
  "account_id": "acc_...",
  "name": "My API Key"
}
```

#### Top Up Account
```bash
POST /admin/top-up
Content-Type: application/json

{
  "account_id": "acc_...",
  "amount": 50.0
}
```

#### Get Account Details
```bash
GET /admin/accounts/{account_id}
```

### User Endpoints

#### List Available Models
```bash
GET /v1/models
Authorization: Bearer beaver_your_api_key
```

#### Chat Completion
```bash
POST /v1/models/{model_id}/chat
Authorization: Bearer beaver_your_api_key
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "temperature": 0.7,
  "max_tokens": 512
}
```

**Example with model:**
```bash
curl -X POST "http://localhost:8000/v1/models/gpt-4o-mini/chat" \
  -H "Authorization: Bearer beaver_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

#### Check Balance
```bash
GET /account/balance
Authorization: Bearer beaver_your_api_key
```

#### Get Transaction History
```bash
GET /account/transactions?limit=50
Authorization: Bearer beaver_your_api_key
```

## 🤖 Supported Models

### OpenAI
- `gpt-4o` - Premium model
- `gpt-4o-mini` - Budget-friendly option
- `gpt-4-turbo` - High-performance model
- `gpt-3.5-turbo` - Cost-effective option

### Anthropic (Claude)
- `claude-3-5-sonnet-20241022` - Latest Sonnet model
- `claude-3-opus-20240229` - Most capable model
- `claude-3-sonnet-20240229` - Balanced performance
- `claude-3-haiku-20240307` - Fast and affordable

### Google (Gemini)
- `gemini-pro` - General purpose model
- `gemini-pro-vision` - Vision-enabled model
- `gemini-1.5-pro` - Advanced capabilities
- `gemini-1.5-flash` - Fast and efficient

## 💰 Pricing

Beaver applies a small markup to provider prices based on model category:

- **ULTRA_BUDGET**: 10% markup
- **BUDGET**: 12.5% markup
- **MID_RANGE**: 15% markup
- **PREMIUM**: 5.5% markup
- **ULTRA_PREMIUM**: 3.5% markup

Pricing is calculated per 1M tokens (input and output separately). Your balance is automatically deducted after each successful API call.

## 🔒 Security

- API keys are validated on every request
- Account balance is checked before processing requests
- Rate limiting prevents abuse
- Usage limits per account plan
- All transactions are logged

## 📊 Usage Tracking

Every API call is logged with:
- Model used
- Input/output tokens
- Cost incurred
- Timestamp
- Account and API key information

## 🗄️ Database & Migrations

Beaver uses **Alembic** for database migrations, supporting both SQLite (development) and PostgreSQL (production).

### Database Configuration

The database URL is configured via environment variable:

```env
# SQLite (default, for development)
# DATABASE_URL not set, or:
DATABASE_URL=sqlite:///./beaver.db

# PostgreSQL (for production)
DATABASE_URL=postgresql+psycopg2://user:password@localhost/beaver
```

### Migration Commands

**Create a new migration:**
```bash
python -m alembic revision --autogenerate -m "Description of changes"
```

**Apply all pending migrations:**
```bash
python -m alembic upgrade head
```

**Rollback one migration:**
```bash
python -m alembic downgrade -1
```

**View current migration status:**
```bash
python -m alembic current
```

**View migration history:**
```bash
python -m alembic history
```

### Initial Setup

For a fresh installation:
```bash
# Install dependencies (includes alembic)
pip install -r requirements.txt

# Create initial migration
python create_initial_migration.py

# Apply migrations
python -m alembic upgrade head
```

### Existing Database

If you have an existing database with tables:
```bash
# Mark current state as baseline (no migration needed)
python -m alembic stamp head

# Future changes will create new migrations
python -m alembic revision --autogenerate -m "Description"
python -m alembic upgrade head
```

### PostgreSQL Migration

To migrate from SQLite to PostgreSQL:

1. **Backup your SQLite database:**
   ```bash
   cp beaver.db beaver.db.backup
   ```

2. **Set PostgreSQL URL:**
   ```env
   DATABASE_URL=postgresql+psycopg2://user:password@localhost/beaver
   ```

3. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE beaver;
   ```

4. **Run migrations:**
   ```bash
   python -m alembic upgrade head
   ```

5. **Migrate data** (use a tool like `pgloader` or custom script)

### Model Changes

When modifying models in `app/database/models.py`:

1. **Generate migration:**
   ```bash
   python -m alembic revision --autogenerate -m "Add new field"
   ```

2. **Review the generated migration** in `alembic/versions/`

3. **Apply migration:**
   ```bash
   python -m alembic upgrade head
   ```

### Migration Safety

- ✅ All migrations are reversible (downgrade supported)
- ✅ Non-destructive by default (additive changes)
- ✅ Type-safe column changes
- ✅ Foreign key constraints enforced
- ✅ Indexes preserved

### Database Models

Current tables:
- `accounts` - User accounts with balance
- `api_keys` - API keys linked to accounts
- `usage_logs` - Request logging
- `transactions` - Balance transactions
- `refresh_tokens` - JWT refresh tokens
- `models` - LLM model registry with pricing

## 🛠️ Development

### Project Structure

```
Beaver/
├── app/
│   ├── auth/           # Authentication logic
│   ├── core/            # Core utilities (rate limiting, usage tracking)
│   ├── database/        # Database models and setup
│   ├── middleware/      # Request middleware
│   ├── models/          # Model registry
│   ├── pricing/         # Pricing engine
│   ├── providers/       # LLM provider integrations
│   ├── routes/          # API routes
│   ├── schemas/         # Pydantic schemas
│   └── usage/           # Usage logging
├── alembic/             # Database migrations
│   ├── versions/       # Migration files
│   └── env.py          # Alembic configuration
├── alembic.ini          # Alembic settings
├── init_db.py           # Database initialization (legacy)
├── create_initial_migration.py  # Create first migration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding a New Provider

1. Create a new provider file in `app/providers/`:
```python
# app/providers/new_provider.py
async def call_new_provider(model, messages, temperature, max_tokens, client):
    # Implementation
    pass
```

2. Add provider models to `app/models/registry.py`

3. Update `app/routes/chat.py` to handle the new provider

4. Add provider API key to `app/config.py`

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

