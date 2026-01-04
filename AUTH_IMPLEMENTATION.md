# 🔐 Password-Based Authentication with JWT Implementation

## Overview

Beaver now supports secure password-based authentication with JWT tokens, while maintaining backward compatibility with API key authentication for LLM usage.

## Architecture

### Dual Authentication System

1. **JWT Authentication** (for user-facing endpoints)
   - Password-based login
   - Short-lived access tokens (15 minutes)
   - Long-lived refresh tokens (30 days)
   - Used for: `/account/*`, `/users/*`, `/api-keys/*`, `/auth/me`

2. **API Key Authentication** (for LLM usage)
   - Unchanged from previous implementation
   - Used for: `/v1/models/*`, chat completions
   - Both auth methods work side-by-side

## Database Changes

### New Fields in `accounts` Table
- `password_hash` (TEXT, nullable) - Bcrypt hashed password
- `email_verified` (BOOLEAN, default FALSE) - Email verification status

### New Table: `refresh_tokens`
- Stores refresh tokens for revocation
- Links to accounts via `account_id`
- Tracks expiration and revocation status

## Security Features

### Password Security
- ✅ Bcrypt hashing with salt
- ✅ Password strength validation (min 8 chars, uppercase, lowercase, digit)
- ✅ Never stored in plaintext
- ✅ Never logged or returned in responses

### JWT Security
- ✅ HS256 algorithm
- ✅ Configurable secret (must be set in `.env`)
- ✅ Token type validation (access vs refresh)
- ✅ Expiration enforcement
- ✅ Refresh token revocation

## API Endpoints

### Registration
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "initial_balance": 0.0
}
```

**Response:**
```json
{
  "account": {
    "id": "acc_...",
    "email": "user@example.com",
    "balance": 0.0,
    "email_verified": false
  },
  "api_key": "beaver_...",
  "api_key_id": "...",
  "message": "Account created successfully. Please login to get JWT tokens."
}
```

**Note:** Registration does NOT issue JWT tokens. User must login.

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

**Response:** Same as login (new access + refresh tokens)

### Logout
```http
POST /auth/logout
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Also works with:**
```http
GET /auth/me
Authorization: Bearer <api_key>
```

Supports both JWT and API key authentication.

## Configuration

### Environment Variables

Add to your `.env` file:

```env
# JWT Settings
JWT_SECRET=your-secret-key-here-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30
```

**Generate a secure JWT secret:**
```bash
openssl rand -hex 32
```

## Migration

### Running the Migration

1. **Option 1: Use the migration script (recommended for existing databases)**
   ```bash
   python migrate_add_password_auth.py
   ```

2. **Option 2: Recreate database (for fresh installs)**
   ```bash
   python init_db.py
   ```

### Migration Script Features
- ✅ Safe migration (checks if already applied)
- ✅ Adds `password_hash` column (nullable for backward compatibility)
- ✅ Adds `email_verified` column
- ✅ Creates `refresh_tokens` table
- ✅ Creates indexes for performance

## Usage Examples

### Frontend Integration

#### 1. Register New User
```typescript
const response = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123'
  })
});

const data = await response.json();
// Store API key for LLM usage
localStorage.setItem('api_key', data.api_key);
```

#### 2. Login
```typescript
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123'
  })
});

const { access_token, refresh_token } = await response.json();
// Store tokens
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);
```

#### 3. Make Authenticated Request
```typescript
const response = await fetch('http://localhost:8000/account/balance', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});
```

#### 4. Refresh Token
```typescript
const response = await fetch('http://localhost:8000/auth/refresh', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    refresh_token: localStorage.getItem('refresh_token')
  })
});

const { access_token, refresh_token } = await response.json();
// Update stored tokens
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);
```

## Backward Compatibility

### Existing Users
- ✅ Accounts without `password_hash`` can still use API keys
- ✅ API key authentication unchanged
- ✅ All existing endpoints work as before

### New Users
- ✅ Must register with password
- ✅ Can use JWT tokens for user endpoints
- ✅ Can still use API keys for LLM usage

## Security Best Practices

1. **JWT Secret**
   - Use a strong, random secret
   - Never commit to version control
   - Rotate periodically in production

2. **Password Requirements**
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one digit
   - Consider adding special characters in future

3. **Token Storage**
   - Store tokens securely (httpOnly cookies recommended for production)
   - Never expose refresh tokens in URLs
   - Implement token rotation

4. **Error Messages**
   - Generic error messages prevent email enumeration
   - "Invalid email or password" for both cases

## Testing

### Manual Testing

1. **Register:**
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"Test1234"}'
   ```

2. **Login:**
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"Test1234"}'
   ```

3. **Use Access Token:**
   ```bash
   curl http://localhost:8000/auth/me \
     -H "Authorization: Bearer <access_token>"
   ```

4. **Refresh Token:**
   ```bash
   curl -X POST http://localhost:8000/auth/refresh \
     -H "Content-Type: application/json" \
     -d '{"refresh_token":"<refresh_token>"}'
   ```

## Files Changed/Created

### New Files
- `app/auth/password.py` - Password hashing utilities
- `app/auth/jwt.py` - JWT token utilities
- `app/auth/dependencies.py` - Authentication dependencies
- `migrate_add_password_auth.py` - Database migration script
- `AUTH_IMPLEMENTATION.md` - This file

### Modified Files
- `app/database/models.py` - Added password_hash, email_verified, RefreshToken model
- `app/routes/auth.py` - Updated registration/login with password and JWT
- `app/routes/users.py` - Updated to support JWT auth
- `app/routes/account.py` - Updated to support JWT auth
- `app/routes/api_keys.py` - Updated to support JWT auth
- `app/config.py` - Added JWT configuration
- `init_db.py` - Added RefreshToken model
- `requirements.txt` - Added bcrypt and pyjwt

## Next Steps (Not Implemented)

- [ ] Email verification
- [ ] Password reset flow
- [ ] OAuth integration (Google, GitHub)
- [ ] 2FA/MFA support
- [ ] Token rotation
- [ ] Rate limiting on auth endpoints
- [ ] Account lockout after failed attempts

## Troubleshooting

### "JWT_SECRET not set"
- Add `JWT_SECRET` to your `.env` file
- Generate with: `openssl rand -hex 32`

### "Invalid token"
- Check token expiration
- Verify JWT_SECRET matches
- Ensure token type matches (access vs refresh)

### "Password too weak"
- Minimum 8 characters
- Must include uppercase, lowercase, and digit

### Migration errors
- Ensure database is not locked
- Check if columns already exist
- Run migration script with proper permissions

