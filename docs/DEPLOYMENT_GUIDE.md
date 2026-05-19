# Deployment Guide: Render (Backend) + Vercel (Frontend)

This guide covers deploying the Zomato AI Recommendation system with:
- **Backend:** FastAPI on Render (free tier)
- **Frontend:** Next.js on Vercel (free tier)

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│  Vercel (Frontend Next.js)          │
│  https://zomato-ai.vercel.app       │
└──────────────┬──────────────────────┘
               │
               │ CORS + API calls
               ▼
┌─────────────────────────────────────┐
│  Render (Backend FastAPI)           │
│  https://zomato-ai-backend.onrender │
│  POST /api/recommend                │
│  GET  /health                       │
└─────────────────────────────────────┘
```

---

## Part 1: Deploy Backend on Render

### Step 1: Connect GitHub to Render

1. Go to https://dashboard.render.com
2. Click **New** → **Web Service**
3. Click **Connect a repository**
4. Authorize GitHub and select `Milestone1-zomato`
5. Click **Connect**

### Step 2: Configure the Service

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `zomato-ai-backend` |
| **Runtime** | `Python 3` |
| **Root Directory** | `.` (leave blank) |
| **Build Command** | `pip install -e .` |
| **Start Command** | `uvicorn milestone_zomato_api.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |

### Step 3: Add Environment Variables

In the **Environment** section, add:

```
GROQ_API_KEY=<your_groq_api_key>
ZOMATO_LLM_PROVIDER=groq
ZOMATO_LLM_MODEL=llama-3.3-70b-versatile
ZOMATO_FILTER_TOP_K=50
ZOMATO_RESTAURANT_CACHE_PATH=data/cache/restaurants.parquet
```

**⚠️ Important:** 
- Get `GROQ_API_KEY` from https://console.groq.com/keys
- Never commit `.env` — add secrets via Render dashboard only

### Step 4: Deploy

1. Click **Create Web Service**
2. Wait 2–3 minutes for build and deployment
3. Once live, note the public URL (e.g., `https://zomato-ai-backend.onrender.com`)
4. Test health check: `https://zomato-ai-backend.onrender.com/health`
   - Should return: `{"status": "healthy", ...}`

### Step 5: Configure CORS

The backend (`backend/src/milestone_zomato_api/main.py`) already includes CORS for Vercel:

```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:8501",
    "*.vercel.app",
    "*.onrender.com",
]
```

No changes needed unless you use a custom domain.

---

## Part 2: Deploy Frontend on Vercel

### Step 1: Connect GitHub to Vercel

1. Go to https://vercel.com
2. Click **Add New** → **Project**
3. Click **Import Git Repository**
4. Select `Milestone1-zomato`
5. Click **Import**

### Step 2: Configure the Project

Vercel auto-detects Next.js. Fill in:

| Field | Value |
|-------|-------|
| **Framework Preset** | `Next.js` |
| **Root Directory** | `frontend-next` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `.next` (default) |

### Step 3: Add Environment Variables

In **Environment Variables**, add:

```
NEXT_PUBLIC_API_URL=https://zomato-ai-backend.onrender.com
```

This tells the frontend where the backend is located.

### Step 4: Deploy

1. Click **Deploy**
2. Wait 1–2 minutes for build
3. Once live, you'll get a Vercel URL (e.g., `https://zomato-ai-nextleap.vercel.app`)
4. Click the URL to view the app

---

## Part 3: Verify End-to-End

### Test the API connection:

1. Open your Vercel frontend URL
2. Fill in:
   - **City:** Bangalore
   - **Budget:** 800
   - **Cuisine:** Italian
   - **Minimum Rating:** 4.0
3. Click **Find Flavors**

### Expected flow:

1. Frontend sends `POST` to backend `/api/recommend`
2. Backend filters restaurants and calls Groq LLM
3. Returns ranked results with explanations
4. Frontend displays styled cards

### If it fails:

- **"API DOWN":** Render backend is sleeping (free tier cold start ~30s)
  - Solution: Wait 30 seconds and retry
- **CORS error:** Backend URL not in `allow_origins`
  - Solution: Update `milestone_zomato_api/main.py` and redeploy
- **No results:** Backend data file missing
  - Solution: Run `python -m milestone_zomato_ingestion` locally to generate `data/cache/restaurants.parquet`

---

## Part 4: Ongoing Maintenance

### Push code updates:

```bash
git add .
git commit -m "Update recommendation logic"
git push origin main
```

Both Render and Vercel auto-redeploy on push (with `autoDeploy: true` in `render.yaml`).

### Monitor logs:

- **Render:** Dashboard → Service → **Logs**
- **Vercel:** Dashboard → Project → **Deployments** → **Logs**

### Scale up (optional):

- **Render:** Upgrade to paid plan for better cold start
- **Vercel:** Upgrade for priority support (optional)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend 503 after 15 mins | Free tier spins down. Wait ~30s for cold start. |
| Frontend won't load | Check `NEXT_PUBLIC_API_URL` in Vercel env vars. |
| Search returns "No results" | Check `data/cache/restaurants.parquet` exists; regenerate if needed. |
| Groq API errors | Verify `GROQ_API_KEY` is valid in Render dashboard. |

---

## Shared URLs

Once deployed, share these links:

- **Frontend:** `https://zomato-ai-nextleap.vercel.app`
- **Backend API:** `https://zomato-ai-backend.onrender.com`
- **Health check:** `https://zomato-ai-backend.onrender.com/health`

---

## Cost Breakdown

| Service | Tier | Cost | Notes |
|---------|------|------|-------|
| Render (Backend) | Free | $0 | Spins down after 15 mins of inactivity |
| Vercel (Frontend) | Free | $0 | Auto-scales, fast cold start |
| Groq API | Free | $0 | Rate-limited; upgrade for production |
| **Total** | — | **$0** | Perfect for demo/coursework |

---

*Last updated: 19 May 2026*
