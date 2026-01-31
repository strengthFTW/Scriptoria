# Scriptoria 🎬

**Minimal Indie Editorial UI + AI-Powered Film Pre-Production**

Scriptoria is a professional workspace for filmmakers and writers. It transforms story ideas into complete screenplay outlines, character profiles, scene breakdowns, and sound design blueprints using lightening-fast AI.

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- 🎭 **Dual Mode Creativity**: 
  - **Generate Mode**: Craft complex screenplays from simple story ideas.
  - **Analyze Mode**: Extract structure and themes from existing draft scripts.
- 📖 **Cinematic Outlining**: AI-powered 3-act structure with precise plot points.
- 👥 **Character Blueprints**: Deep character arcs and personality profiles.
- 🎬 **Scene Breakdown**: Scene-by-scene analysis with cast lists and locations.
- 🔊 **Sonic Architecture**: Ambient themes and sound design recommendations.
- 🎨 **Indie Editorial UI**: A calm, tactile, writer-focused workspace inspired by vintage print.
- ⚡ **Turbo Inference**: Powered by **Groq AI** for near-instant (70B) generation.
- � **Secure Persistence**: Full user authentication and story storage via **Supabase**.
- 📄 **Production Export**: One-click PDF generation for sharing with your crew.

---

## �️ Tech Stack

### Backend
- **Flask**: Python-based API orchestration.
- **Groq AI**: Llama-3.3-70B model for high-fidelity writing.
- **Python 3.10+**: Core logic and text processing.

### Frontend
- **React 19**: Modern UI component architecture.
- **Supabase**: Managed Authentication and PostgreSQL database.
- **Vite 6**: Lightning-fast build and development server.
- **CSS3**: Custom "Editorial Indie" design system (No Tailwind dependencies).

---

## 🚀 Installation & Setup

### 1. Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://www.python.org/) (v3.10+)
- [Groq API Key](https://console.groq.com/) (Free)
- [Supabase Project](https://supabase.com/) (Free)

### 2. Backend Configuration
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
python app.py
```

### 3. Frontend Configuration
```bash
cd frontend
npm install

# Create .env file
cat <<EOF > .env
VITE_API_URL=http://localhost:5000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
EOF

npm run dev
```

---

## 🎨 Design Philosophy

Scriptoria follows a **Minimal Indie Editorial** aesthetic:
- **Paper Finish**: Warm cream backgrounds (#f5f1e8) and light manuscript cards.
- **Ink Typography**: Sharp Charcoal ink (#2b2b2b) using *IBM Plex Mono* and *Inter*.
- **Tactile Depth**: Solid offset shadows and subtle paper grain textures.
- **Calm Interaction**: Muted coral accents (#d66d53) for focus states.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for filmmakers and storytellers.**
🎬 *Scriptoria: From idea to blueprint in seconds.*
