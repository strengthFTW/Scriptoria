# Scriptoria - Quick Start Guide

## 🆕 AI Integration Setup (Required)

### Get Gemini API Key
1. Visit https://aistudio.google.com/app/apikey
2. Sign in and create API key (free tier: 15 req/min)
3. Copy the key

### Configure Backend
Create `backend/.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
FLASK_ENV=development
```

### Install AI Dependencies
```bash
cd backend
venv\Scripts\activate
pip install google-generativeai==0.8.0
```

## Quick Commands

### Start Backend (Terminal 1)
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs on: http://localhost:5000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: http://localhost:5173

### First Time Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## Testing the App

1. Open http://localhost:5173 in your browser
2. Enter a story idea (20-500 characters)
3. Select a genre
4. Click "Generate Screenplay"
5. View the mock results showing screenplay structure and characters

## Project Structure

```
Scriptoria/
├── backend/
│   ├── app.py              # Flask server with /generate endpoint
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   └── App.css        # Indie light retro styling
│   └── package.json       # Node dependencies
│
└── README.md              # Project documentation
```

## Current Features (MVP)

✅ Flask backend with mock API  
✅ React frontend with beautiful UI  
✅ Indie light theme with retro fonts  
✅ Form validation and error handling  
✅ Loading states  
✅ Mock screenplay generation  
✅ Character profiles  

## Next Steps for Full Implementation

1. **Add AI Integration**: Integrate Google Gemini or OpenAI API
2. **Scene Generation**: Add scene breakdown generator
3. **Sound Design**: Add sound design suggestions
4. **Save Projects**: Implement JSON storage
5. **Export Features**: Add PDF/JSON export

## Troubleshooting

**Backend won't start:**
- Make sure port 5000 is available
- Check that Flask is installed: `pip list | findstr Flask`

**Frontend won't connect:**
- Verify backend is running at http://localhost:5000
- Check browser console for CORS errors
- Try clearing browser cache

**CORS Errors:**
- Backend already has `flask-cors` enabled
- Make sure both servers are running

---

**Ready to generate your first screenplay!** 🎬✨
