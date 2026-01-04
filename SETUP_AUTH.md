# 🚀 Quick Setup Guide: Password Authentication

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `bcrypt` - Password hashing
- `pyjwt` - JWT token handling

## Step 2: Set JWT Secret

Add to your `.env` file:

```env
JWT_SECRET=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30
```

**Generate a secure secret:**
```bash
openssl rand -hex 32
```

## Step 3: Run Migration

For existing databases:
```bash
python migrate_add_password_auth.py
```

For fresh installs:
```bash
python init_db.py
```

## Step 4: Start Server

```bash
uvicorn app.main:app --reload
```

## Step 5: Test Authentication

### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234"}'
```

Save the `access_token` from the response.

### Use Token
```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## ✅ Done!

Your authentication system is now ready. See `AUTH_IMPLEMENTATION.md` for full documentation.

