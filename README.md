# HealthAI 🏥

> AI-powered healthcare assistant with medical document intelligence, lab trend analysis, nutrition planning, and smart notifications.

## 🚀 Features

- **AI Chat** — Health-aware multi-turn conversations with clinical triage
- **Medical Document Intelligence** — Upload PDFs, images, lab reports; auto OCR + AI analysis
- **Health Timeline** — Auto-populated from every document and consultation
- **Lab Trend Comparison** — Track lab values over time with trend analysis
- **Health Memory** — AI remembers your medical history across sessions
- **Nutrition & Diet Planning** — Personalized meal plans based on your health profile
- **PDF Report Generation** — Auto-generates branded PDF after every document analysis
- **Email + SMS Notifications** — Verification, device alerts, report notifications
- **Premium Settings** — 8-tab account center with glassmorphism UI

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS, Framer Motion |
| Backend | FastAPI, SQLAlchemy, SQLite/PostgreSQL |
| AI | Google Gemini API |
| Auth | JWT + bcrypt |
| Email | Resend API |
| SMS | Twilio |

## ⚙️ Local Setup

### Backend
```bash
cd backend
cp .env.example .env
# Fill in your API keys in .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
cp .env.example .env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8001
npm install
npm run dev
```

App: http://localhost:3000  
API Docs: http://localhost:8001/docs

## 🌐 Deployment

- **Frontend**: Deploy `/frontend` on [Vercel](https://vercel.com)
- **Backend**: Deploy `/backend` on [Render](https://render.com) or [Railway](https://railway.app)

See deployment guides below.

## 📁 Project Structure

```
healthAi/
├── backend/          FastAPI Python API
│   ├── routes/       API endpoints
│   ├── services/     Business logic (28 services)
│   ├── templates/    HTML email templates
│   └── main.py       App entry point
└── frontend/         Next.js application
    ├── app/          Pages (App Router)
    └── components/   Reusable UI components
```

## 🔐 Environment Variables

See `backend/.env.example` and `frontend/.env.example` for required variables.
