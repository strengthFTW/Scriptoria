# 🚀 Deployment Guide for Scriptoria

## Architecture
- **Frontend (React)**: Vercel
- **Backend (Flask)**: Render (free tier)

---

## 📦 Step 1: Deploy Backend to Render

### A. Sign up for Render
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Connect your GitHub repository: `strengthFTW/Scriptoria`

### B. Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Select your `Scriptoria` repository
3. Configure:
   ```
   Name: scriptoria-backend
   Root Directory: backend
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Instance Type: Free
   ```

### C. Add Environment Variables
In Render dashboard, add:
```
GROQ_API_KEY=your_groq_api_key_here
```

### D. Deploy
1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. Copy your backend URL (e.g., `https://scriptoria-ua29.onrender.com`)

---

## 🎨 Step 2: Deploy Frontend to Vercel

### A. Update Frontend API URL
1. Go to `frontend/src/App.jsx`
2. Change line 5:
   ```javascript
   const API_BASE = 'https://scriptoria-ua29.onrender.com';
   ```

### B. Commit and Push
```bash
git add .
git commit -m "Update API endpoint for production"
git push origin main
```

### C. Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account
3. Click **"Add New Project"**
4. Import `strengthFTW/Scriptoria`
5. Configure:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```
6. Click **"Deploy"**
7. Wait 1-2 minutes

### D. Get Your Live URL
- Your app will be live at: `https://scriptoria-xxx.vercel.app`

---

## ✅ Verification Steps

1. **Test Backend**:
   ```bash
   curl https://scriptoria-ua29.onrender.com/health
   ```
   Should return: `{"status": "healthy"}`

2. **Test Frontend**:
   - Visit your Vercel URL
   - Try generating a screenplay
   - Test file upload
   - Test PDF export

---

## 🔧 Environment Variables

### Backend (Render)
- `GROQ_API_KEY` - Your Groq API key

### Frontend (Vercel)
- None needed (API URL is in code)

---

## 📝 Important Notes

1. **First Load**: Render free tier sleeps after 15 min inactivity. First request may take 30-60 seconds.
2. **CORS**: Already configured in `backend/app.py`
3. **File Uploads**: Work on Render (ephemeral storage)
4. **PDF Export**: Works perfectly

---

## 🔄 Future Updates

To deploy updates:

**Backend:**
```bash
git push origin main
# Render auto-deploys from GitHub
```

**Frontend:**
```bash
git push origin main
# Vercel auto-deploys from GitHub
```

---

## 🆘 Troubleshooting

### Backend Issues
- Check Render logs: Dashboard → Logs
- Verify GROQ_API_KEY is set
- Ensure `requirements.txt` is in `/backend`

### Frontend Issues
- Check Vercel logs: Dashboard → Deployments → Logs
- Verify API_BASE URL is correct
- Check browser console for CORS errors

### CORS Errors
- Ensure backend CORS allows your Vercel domain
- Update `app.py` if needed

---

## 💰 Cost
- **Render Backend**: $0/month (free tier)
- **Vercel Frontend**: $0/month (hobby tier)
- **Total**: FREE! 🎉

---

## 🔗 Your Deployed URLs

After deployment, update these:
- **Frontend**: https://scriptoria-xxx.vercel.app
- **Backend**: https://scriptoria-ua29.onrender.com
- **GitHub**: https://github.com/strengthFTW/Scriptoria

---

Enjoy your deployed Scriptoria app! 🎬✨
