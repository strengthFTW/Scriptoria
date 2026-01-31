# Scriptoria - Quick Start Guide ⚡

Follow these steps to get your local development environment running in under 5 minutes.

## 1. Prerequisites
- **Node.js 18+** & **npm**
- **Python 3.10+**
- **Groq API Key**: Get it for free at [console.groq.com](https://console.groq.com/)
- **Supabase Project**: Create a free project at [supabase.com](https://supabase.com/)

---

## 2. Backend Setup (Flask)
The backend handles the AI generation and PDF exports.

```bash
cd backend
python -m venv venv
# Activate venv:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
```

### Configure Environment
Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_gsk_api_key_here
```

### Start Server
```bash
python app.py
```
> Server will run at: `http://localhost:5000`

---

## 3. Frontend Setup (React + Vite)
The frontend provides the "Indie Editorial" workspace.

```bash
cd frontend
npm install
```

### Configure Environment
Create a `.env` file in the `frontend/` directory:
```env
VITE_API_URL=http://localhost:5000
VITE_SUPABASE_URL=your_project_url_from_supabase
VITE_SUPABASE_ANON_KEY=your_anon_public_key_from_supabase
```

### Start Development Server
```bash
npm run dev
```
> Workspace will be available at: `http://localhost:5173`

---

## 4. Database Setup (Supabase)
To enable the **Save/Load** functionality, run the following SQL in your Supabase SQL Editor:

```sql
create table stories (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null,
  title text not null,
  genre text,
  story_idea text,
  screenplay jsonb not null,
  characters jsonb not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable Row Level Security
alter table stories enable row level security;

-- Create Policy: Users can only see their own stories
create policy "Users can manage their own stories"
  on stories for all
  using (auth.uid() = user_id);
```

---

## 5. Troubleshooting
- **CORS Errors**: Ensure the backend's `CORS` origins in `app.py` allow your frontend URL.
- **Save Failed**: Check that your Supabase URL and Key are correct in `frontend/.env`.
- **AI Typos**: Scriptoria uses Llama-3.3-70B on Groq; ensure your API key has "versatile" model access.

🎬 **Happy Writing!**
