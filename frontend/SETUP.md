# 🚀 Frontend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

The `.env.local` file is already created with:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Start Backend (in another terminal)

```bash
cd ..
uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js pages
│   │   ├── page.tsx           # Homepage
│   │   ├── auth/              # Login/Register
│   │   ├── dashboard/         # Dashboard pages
│   │   ├── playground/        # Chat playground
│   │   └── models/            # Models list page
│   ├── components/            # React components
│   │   ├── Navigation.tsx     # Top navigation
│   │   ├── Hero.tsx           # Hero section
│   │   ├── Models.tsx         # Models list
│   │   ├── Features.tsx        # Features section
│   │   ├── FlowDiagram.tsx    # How it works
│   │   ├── CTA.tsx            # Call to action
│   │   └── Footer.tsx         # Footer
│   └── config/
│       └── api.ts             # API helper functions
├── package.json
└── tailwind.config.js
```

## Features Implemented

✅ **Homepage**
- Hero section with dynamic stats
- Features showcase
- Flow diagram
- Models list
- Call to action

✅ **Authentication**
- Login page (`/auth/login`)
- Register page (`/auth/register`)
- Auto-redirect if not authenticated

✅ **Dashboard**
- Main dashboard (`/dashboard`)
- Balance display
- Usage stats
- Quick actions

✅ **API Key Management**
- List API keys (`/dashboard/keys`)
- Create new keys
- Delete keys
- Copy new keys

✅ **Chat Playground**
- Model selector
- Chat interface
- Real-time messaging
- Error handling

✅ **Usage Analytics**
- Usage stats (`/dashboard/usage`)
- Billing history
- Model breakdown

## Testing the Frontend

1. **Start both servers:**
   ```bash
   # Terminal 1: Backend
   uvicorn app.main:app --reload
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

2. **Test Flow:**
   - Visit `http://localhost:3000`
   - Click "Get Started" or "Sign In"
   - Register with email
   - Should redirect to dashboard
   - Check balance shows in navigation
   - Go to API Keys page
   - Create a new key
   - Go to Playground
   - Select a model and send a message

## Troubleshooting

### Frontend won't start
- Check Node.js version: `node --version` (need 18+)
- Delete `node_modules` and `package-lock.json`, then `npm install`

### Can't connect to backend
- Verify backend is running on port 8000
- Check `.env.local` has correct API URL
- Check browser console for CORS errors

### API calls failing
- Check API key is stored: `localStorage.getItem('beaver_api_key')`
- Verify backend is running
- Check network tab in browser dev tools

## Production Build

```bash
# Build
npm run build

# Start production server
npm start
```

## Deployment

Deploy to Vercel, Netlify, or any Next.js-compatible platform:

1. Update `NEXT_PUBLIC_API_URL` to production backend URL
2. Build: `npm run build`
3. Deploy

The frontend is ready to use! 🎉

