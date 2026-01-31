# Scriptoria - Production Deployment Guide 🚀

This guide outlines how to deploy the full-stack Scriptoria workspace to production using **Render** (Backend) and **Vercel** (Frontend).

## 🌍 Architecture Overview
- **Storage/Auth**: Supabase (Cloud)
- **AI Engine**: Groq (API)
- **Backend**: Render (Web Service)
- **Frontend**: Vercel (Static Site)

---

## 🏗️ Step 1: Deploy Backend (Render)

1. **Connect Repository**: Link your GitHub repo to [Render](https://render.com).
2. **Create Web Service**:
   - **Name**: `scriptoria-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
3. **Environment Variables**:
   Add these in the Render dashboard:
   - `GROQ_API_KEY`: Your production API key.
   - `DATABASE_URL`: (Optional) If using a separate backend DB.
4. **Copy URL**: Save your new Render URL (e.g., `https://scriptoria-api.onrender.com`).

---

## 🎨 Step 2: Deploy Frontend (Vercel)

1. **Connect Repository**: Link your GitHub repo to [Vercel](https://vercel.com).
2. **Configure Project**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. **Environment Variables**:
   Add these in the Vercel project settings:
   - `VITE_API_URL`: Your Render backend URL.
   - `VITE_SUPABASE_URL`: Your Supabase Project URL.
   - `VITE_SUPABASE_ANON_KEY`: Your Supabase Anon Key.
4. **Deploy**: Click deploy and get your live `.vercel.app` URL.

---

## 🔐 Step 3: Configure Supabase

1. **Auth Settings**:
   Add your Vercel URL to the **Site URL** and **Redirect URLs** in the Supabase Auth Settings.
2. **CORS**:
   (Optional) If you face CORS issues, add your Vercel domain to the `CORS` setup in `backend/app.py`.

---

## ✅ Post-Deployment Checklist
- [ ] Test **Login/Register** flow.
- [ ] Verify **Screenplay Generation** calls the live Render API.
- [ ] Confirm **Save to Library** persists data to Supabase.
- [ ] Test **PDF Export** download.

---

## 💡 Pro-Tips
- **Cold Starts**: Render's free tier "sleeps" after 15 minutes. The first API call might take ~30 seconds to wake up.
- **Logs**: Use `vercel logs` and Render's **Events** tab to debug production issues.

🎬 **Scriptoria is now live for the world to use!**
