# 🚀 Quick Start Guide

Get your Beaver API Gateway up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Environment

Create a `.env` file in the root directory:

```env
APP_NAME=beaver
ENV=dev
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here  # Optional
GOOGLE_API_KEY=your_google_key_here  # Optional
```

**Note:** You need at least `OPENAI_API_KEY` to use OpenAI models. Other keys are optional.

## Step 3: Initialize Database

```bash
python init_db.py
```

This creates all necessary database tables.

## Step 4: Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Step 5: Test the Connection

Open a new terminal and run:

```bash
python test_api.py
```

This will:
- ✅ Test health endpoint
- ✅ Verify CORS configuration
- ✅ Create a test account
- ✅ Create an API key
- ✅ Test listing models
- ✅ Test balance check

## Step 6: Connect Your Frontend

Your Lovable frontend at `https://beaver-ai-hub.lovable.app` is already configured to work with this backend!

### In your frontend code:

1. **Set the API base URL:**
   ```javascript
   const API_BASE_URL = 'http://localhost:8000'; // Development
   // or 'https://your-backend-domain.com' for production
   ```

2. **Use the API key from the test:**
   ```javascript
   const API_KEY = 'beaver_...'; // From test_api.py output
   ```

3. **Make requests:**
   ```javascript
   fetch(`${API_BASE_URL}/v1/models`, {
     headers: {
       'Authorization': `Bearer ${API_KEY}`,
       'Content-Type': 'application/json'
     }
   })
   ```

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Common Issues

### Redis Connection Error
If you don't have Redis installed:
- **Windows:** Download from https://redis.io/download or use Docker
- **Mac:** `brew install redis` then `brew services start redis`
- **Linux:** `sudo apt-get install redis-server` then `sudo systemctl start redis`

### Database Error
Make sure you ran `python init_db.py` before starting the server.

### CORS Error in Frontend
The backend is configured to allow requests from:
- `https://beaver-ai-hub.lovable.app`
- `http://localhost:3000`
- `http://localhost:5173`
- `http://localhost:8080`

If you need to add more origins, edit `app/config.py`.

## Next Steps

1. ✅ Create your first account via `/admin/accounts`
2. ✅ Create an API key via `/admin/api-keys`
3. ✅ Top up your account via `/admin/top-up`
4. ✅ Start making API calls from your frontend!

For detailed API documentation, see [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md)


