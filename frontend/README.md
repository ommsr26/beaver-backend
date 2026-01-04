# Beaver Frontend

Frontend application for Beaver AI - Unified API Gateway for LLMs

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend server running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app router pages
│   │   ├── page.tsx      # Home page
│   │   ├── auth/         # Authentication pages
│   │   └── dashboard/    # Dashboard pages
│   ├── components/       # React components
│   │   ├── Navigation.tsx
│   │   ├── Hero.tsx
│   │   ├── Models.tsx
│   │   └── ...
│   └── config/           # Configuration
│       └── api.ts        # API helper functions
├── public/               # Static assets
└── package.json
```

## Features

- ✅ Homepage with hero, features, models list
- ✅ Authentication (login/register)
- ✅ Dashboard with balance and stats
- ✅ API key management
- ✅ Chat playground
- ✅ Usage analytics
- ✅ Responsive design with Tailwind CSS

## Pages

- `/` - Homepage
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/dashboard` - Main dashboard
- `/dashboard/keys` - API key management
- `/dashboard/usage` - Usage analytics
- `/playground` - Chat playground
- `/models` - Models list (also on homepage)

## Development

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint
npm run lint
```

## Backend Connection

The frontend connects to the backend API at `http://localhost:8000` by default.

All API calls are handled through `src/config/api.ts` which includes:
- Authentication helpers
- API key management
- Account operations
- Model listing
- Chat completions
- Usage tracking

## Deployment

For production deployment:

1. Update `NEXT_PUBLIC_API_URL` to your production backend URL
2. Build the application: `npm run build`
3. Deploy to Vercel, Netlify, or your preferred hosting

