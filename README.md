# Scriptoria 🎬

**AI-Powered Film Pre-Production System**

Transform story ideas into complete screenplay outlines, character profiles, scene breakdowns, and sound design suggestions using AI.

![Scriptoria Demo](https://img.shields.io/badge/Status-Hackathon%20MVP-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- 🎭 **Dual Mode Operation**:
  - **Generate Mode**: Create screenplays from short story ideas
  - **Analyze Mode**: Extract structure from existing scripts
- 📖 **Screenplay Generation**: AI-powered 3-act structure with plot points
- 👥 **Character Profiles**: Detailed character arcs and personality traits
- 🎬 **Scene Breakdown**: Detailed scene-by-scene analysis with cast lists
- 🔊 **Sound Design**: Music themes, SFX, and ambience recommendations
- 🎨 **Indie Light Theme**: Beautiful retro-style UI with colorful fonts
- ⚡ **Fast Generation**: ~5-10 seconds using Groq AI (free!)
- 📱 **Responsive Design**: Works on desktop and tablet
- 📄 **PDF Export**: One-click export of complete production package

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Free Groq API key (no credit card required!)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run server
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on `http://localhost:5173`

## 🔑 Getting a Free Groq API Key

1. Visit https://console.groq.com/
2. Sign up (no credit card required!)
3. Go to "API Keys" section
4. Create a new API key
5. Copy and paste into `backend/.env`:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

**Free tier includes:**
- Unlimited requests (with rate limits)
- Super fast inference (70+ tokens/sec)
- Multiple models available

## 🎯 Usage

### Generate Mode (Create from Idea)
1. Open http://localhost:5173 in your browser
2. Click "📝 Generate from Idea" button
3. Enter your story idea (20-500 characters)
4. Select a genre (Drama, Thriller, Comedy, Sci-Fi, Horror)
5. Click "Generate Breakdown"
6. View AI-generated screenplay and characters!

### Analyze Mode (Existing Script)
1. Open http://localhost:5173 in your browser
2. Click "🎬 Analyze Existing Script" button
3. Paste your complete screenplay (100-100,000 characters) OR upload a PDF/DOCX file
4. Select the genre
5. Click "Analyze & Generate"
6. View extracted structure, characters, scenes, and sound design!

📚 See [SCRIPT_ANALYSIS_GUIDE.md](SCRIPT_ANALYSIS_GUIDE.md) for detailed analysis mode documentation.

## 📁 Project Structure

```
Scriptoria/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example       # Environment template
│   ├── generators/         # AI generation modules
│   │   ├── screenplay_generator.py
│   │   └── character_generator.py
│   └── utils/
│       └── ai_client.py    # Groq API client
│
├── frontend/               # React application
│   ├── src/
│   │   ├── App.jsx        # Main component
│   │   └── App.css        # Indie light retro styling
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

**Backend:**
- Flask 3.0
- Groq AI API (llama-3.3-70b-versatile)
- Python 3.8+

**Frontend:**
- React 19
- Vite 7
- Axios
- Custom CSS (Indie Light Theme)

**Fonts:**
- Fredoka One (titles)
- Righteous (labels)
- Poppins (body text)

## 🎨 Design System

**Color Palette:**
- Cream (#FFF8E7)
- Peach (#FFB5A7)
- Mint (#B4F8C8)
- Coral (#FF6B6B)
- Retro Orange (#FF9F1C)
- Retro Teal (#2EC4B6)
- Retro Purple (#9D4EDD)

## 📝 API Endpoints

### `POST /generate`
Generate screenplay and characters from story idea.

**Request:**
```json
{
  "storyIdea": "A detective who can see ghosts investigates their own murder",
  "genre": "Thriller"
}
```

**Response:**
```json
{
  "success": true,
  "screenplay": {
    "title": "...",
    "logline": "...",
    "threeActStructure": { ... },
    "plotPoints": [ ... ]
  },
  "characters": [ ... ],
  "timestamp": "..."
}
```

### `GET /health`
Health check endpoint.

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Verify virtual environment is activated
- Check `.env` file exists with valid `GROQ_API_KEY`

### Frontend won't connect
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Verify both servers are running

### API errors
- Verify Groq API key is valid
- Check rate limits (free tier has limits)
- Look at backend terminal for detailed error messages

## 🚧 Future Enhancements

- [ ] Scene breakdown generation
- [ ] Sound design suggestions
- [ ] Save/load projects (JSON storage)
- [ ] Export to PDF
- [ ] Storyboard generation
- [ ] Shot list creation
- [ ] Budget estimation
- [ ] Collaboration features

## 📄 License

MIT License - feel free to use for your projects!

## 🤝 Contributing

This is a hackathon MVP. Contributions welcome!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with [Groq](https://groq.com/) - Lightning-fast AI inference
- Inspired by the need for accessible film pre-production tools
- Created during a 24-hour hackathon challenge

---

**Made with ❤️ for filmmakers and storytellers**

🎬 Start creating your screenplay today!
