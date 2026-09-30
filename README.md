# IntelTransform AI — SIH26154

> **Generative AI Platform for Trusted Multi-Format Content Transformation**

---

## 🚀 Quick Start

```powershell
# From the "GenAI Platform" root directory:
.\start.ps1
```

Then open **http://localhost:5173** in your browser.

---

## 📐 Architecture

```
ONE SOURCE  →  AI UNDERSTANDING  →  SOURCE-GROUNDED TRANSFORMATION  →  MULTIPLE OUTPUTS
```

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + TypeScript + Vite + Tailwind CSS |
| Backend | FastAPI (Python) + SQLAlchemy + SQLite |
| AI Engine | Demo Mode (Deterministic) / Gemini API / OpenAI API |
| RAG | In-memory TF-IDF vector store with chunk metadata |
| Exports | ReportLab (PDF), python-docx (DOCX), python-pptx (PPTX) |

---

## 📂 Project Structure

```
GenAI Platform/
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── ai/           # AI provider, demo engine, validator
│   │   ├── api/          # REST endpoints (transform, docs, projects…)
│   │   ├── core/         # Config, database, settings
│   │   ├── exporters/    # PDF, DOCX, PPTX, text exporters
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── rag/          # Vector store & retrieval
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Document parser, audit service
│   ├── venv/             # Python virtual environment
│   └── requirements.txt
├── frontend/             # React TypeScript frontend
│   ├── src/
│   │   ├── components/   # UI components (OutputCard, Sidebar…)
│   │   ├── pages/        # Application pages
│   │   ├── services/     # API client
│   │   └── types/        # TypeScript type definitions
│   └── package.json
├── data/
│   ├── uploads/          # Uploaded source documents
│   └── samples/          # Built-in demo documents
├── exports/              # Generated PDF/DOCX/PPTX artifacts
└── start.ps1             # One-click startup script
```

---

## 🎯 8 Output Formats

| Format | Audience | Description |
|--------|----------|-------------|
| **Executive Summary** | C-Suite | Situation, Key Findings, Impact & Recommendations |
| **Security Advisory** | Defense | CVSS, IoCs, Mitigation Roadmap |
| **Presentation** | Leadership | 16:9 Slide Deck with Speaker Notes |
| **Infographic Blueprint** | Public | Visual flow, metrics callouts |
| **LinkedIn Post** | Professional | Thought leadership post |
| **X/Twitter Thread** | Real-time | 4-part operational thread |
| **Video Package** | Media | Scene-by-scene storyboard + script |
| **Intelligence Brief** | Analysts | Adversary attribution, indicators |

---

## ⚙️ Configuration

### Demo Mode (Default — No API Key Required)
The platform ships with a **high-fidelity deterministic demo engine** that:
- Generates realistic, source-grounded outputs instantly
- Includes source citations, validation scores, and claim analysis
- Works 100% offline — perfect for SIH demonstrations

### Live AI Mode (Optional)
Go to **Settings** in the app and enter your:
- **Gemini API Key** (Google AI Studio) — recommended
- **OpenAI API Key** (OpenAI Platform)

Toggle **Demo Mode OFF** to use live LLM generation with real RAG retrieval.

---

## 🔑 Key Features Demonstrated

- ✅ **Document Ingestion** — PDF, DOCX, TXT upload + chunking
- ✅ **RAG Context Retrieval** — TF-IDF vector store + top-k chunk retrieval  
- ✅ **Multi-Format Generation** — 8 parallel output formats
- ✅ **Source Citations** — Every claim linked to source page/chunk
- ✅ **Validation Engine** — Claim-by-claim consistency scoring
- ✅ **Human Review Workflow** — Edit, approve/reject, version history
- ✅ **Export Pipeline** — One-click PDF, DOCX, PPTX, MD, JSON downloads
- ✅ **Audit Trail** — Immutable compliance logs for all actions
- ✅ **Template Library** — Pre-configured domain transformation templates
- ✅ **Role-Based UI** — Analyst, Reviewer, Admin role switching

---

## 🛠 Manual Setup (If Needed)

```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

---

## 📜 License
Smart India Hackathon 2024 — Problem Statement SIH26154  
Built by IntelTransform AI Team
