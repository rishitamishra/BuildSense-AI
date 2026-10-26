# Multimodal Construction Intelligence Platform

Educational MVP: React + Vite frontend, FastAPI backend, optional Google Gemini multimodal analysis.

## Run it
Requirements: Python 3.9+ (3.11 recommended), Node.js 20+.

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

### Frontend (second terminal)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

### Enable Gemini
Get an API key from Google AI Studio and add it to `backend/.env`:
`GEMINI_API_KEY=your_key_here`
Never commit `.env`. Without a key, the app uses a clearly labelled demo response.

## Demo video (2–3 min)
Show the app, enter project details, upload a site image, run analysis, explain safety/crack results and planning/cost, then show `/docs`. Mention limitations. Record with OBS or your screen recorder, upload as an unlisted YouTube video or shareable Google Drive video, then paste the real URL into SkillWallet.

## GitHub
Create a repository on GitHub, push this folder, then paste the actual repository URL into SkillWallet. The demo/GitHub URLs cannot be generated until you publish them from your accounts.

## Safety disclaimer
This is a student prototype, not a certified safety, structural-engineering, weather, or valuation service. Get qualified professional review before acting on high-risk findings.
