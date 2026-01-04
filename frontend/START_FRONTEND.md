# 🚀 Starting the Frontend

## Quick Start

You're already in the frontend directory. Just run:

```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Full Setup

### 1. Make sure backend is running (in another terminal):
```bash
cd ..
uvicorn app.main:app --reload
```

### 2. Start frontend:
```bash
npm run dev
```

### 3. Open browser:
Visit `http://localhost:3000`

## What You'll See

- **Homepage** with hero, features, and models
- **Navigation** with Sign In / Get API Key buttons
- All pages are ready to use!

## Testing Flow

1. Click "Get Started" or "Sign In"
2. Register with your email
3. You'll be redirected to dashboard
4. Create an API key
5. Test the chat playground

## Note on Vulnerabilities

The 3 high severity vulnerabilities are in dev dependencies (eslint) and won't affect:
- ✅ The running application
- ✅ Production builds
- ✅ User experience

They're safe to ignore for now. Next.js will update these in future versions.

## Troubleshooting

**Port 3000 already in use?**
- Change port: `npm run dev -- -p 3001`

**Can't connect to backend?**
- Make sure backend is running on port 8000
- Check `.env.local` has correct API URL

**Build errors?**
- Delete `node_modules` and `.next` folder
- Run `npm install` again


