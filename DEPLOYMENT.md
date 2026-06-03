# Scriptoria - Production Deployment Guide 🚀

This guide deploys the full-stack Scriptoria app as a **single Render Web Service** that serves both the backend API and the built frontend.

## 🌍 Architecture
- **Storage/Auth**: Supabase (Cloud)
- **AI Engine**: Groq (API)
- **App Host**: Render Web Service (single service, Flask serves React)
- **Frontend**: Built by Render into `frontend/dist`, then served by Flask

---

## 🏗️ Deploy to Render

### Option A — One-click with `render.yaml` (Recommended)
The repo already has a `render.yaml` blueprint. Just:
1. Connect your GitHub repo to [Render](https://render.com).
2. Render will auto-detect the `render.yaml` and configure the service.
3. Set the required environment variables (see below) and deploy.

### Option B — Manual Setup
1. **Create a Web Service** in Render:
   - **Root Directory**: leave blank (top-level)
   - **Environment**: `Python`
   - **Build Command**:
     ```bash
     pip install -r backend/requirements.txt && cd frontend && npm install && npm run build
     ```
   - **Start Command**:
     ```bash
     cd backend && gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 2 app:app
     ```

---

## 🔑 Environment Variables to Set in Render Dashboard

Set these under **Environment → Environment Variables** in your Render service:

| Variable | Value | Notes |
|---|---|---|
| `GROQ_API_KEY` | `gsk_...` | Your Groq API key |
| `JWT_SECRET_KEY` | (random string) | Render can auto-generate this |
| `FLASK_ENV` | `production` | |
| `VITE_SUPABASE_URL` | `https://xxx.supabase.co` | From your Supabase project |
| `VITE_SUPABASE_ANON_KEY` | `eyJ...` | From your Supabase project |

> ⚠️ **CRITICAL**: Do NOT set `VITE_API_URL` on Render.
> The frontend already defaults to relative URLs (`''`) in production,
> which means it calls the same Render service. Setting it to
> `http://localhost:5000` (or anything else) will break it.

---

## 🔐 Configure Supabase

After getting your Render URL (e.g. `https://scriptoria.onrender.com`):

1. Go to your Supabase project → **Authentication → URL Configuration**
2. Set **Site URL** to your Render URL
3. Add your Render URL to **Redirect URLs**

---

## ✅ Post-Deployment Checklist
- [ ] Open your Render URL — you should see the Scriptoria UI (not just JSON)
- [ ] Test **Login/Register** flow
- [ ] Verify **Screenplay Generation** works (calls `/generate`)
- [ ] Test **PDF Export** download
- [ ] Check **Save to Library** persists to Supabase

---

## 🐛 Troubleshooting

**Only seeing JSON / backend response instead of the UI?**
- The `frontend/dist` wasn't built. Check Render build logs for npm errors.
- Make sure the build command runs `cd frontend && npm install && npm run build`.

**Frontend loads but API calls fail?**
- You accidentally set `VITE_API_URL` to something. Remove it from Render env vars.
- The `VITE_*` variables must be set **before** the build runs (they get baked in at build time).

**Auth / Supabase not working?**
- Add your Render URL to Supabase Auth → Redirect URLs.

**Cold starts (first request is slow)?**
- Render free tier sleeps after 15 minutes of inactivity. The first request takes ~30s to wake up. Upgrade to a paid plan to avoid this.

---

💡 **Local development**: Run frontend (`npm run dev`) and backend (`python app.py`) separately.
The production single-service setup only applies on Render.

🎬 **Scriptoria is now live as one Render service!**
