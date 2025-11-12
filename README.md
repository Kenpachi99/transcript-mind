# TranscriptMind

Transform YouTube videos into interactive knowledge bases. Ask questions, get intelligent answers powered by semantic search and local LLMs.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Overview

TranscriptMind is a full-stack application that transcribes YouTube videos and enables semantic Q&A over the content using retrieval-augmented generation (RAG). Built for efficiency and privacy—all processing happens locally with no external LLM API calls.

**Key insight:** Extract actionable insights from long-form video content in seconds instead of hours.

## ✨ Features

- **One-Click Transcription** — Paste a YouTube URL, get accurate transcripts in minutes
- **Semantic Search** — Find relevant sections by meaning, not just keywords
- **Local LLM Inference** — Privacy-first Q&A with no API costs
- **RAG Pipeline** — Augmented generation for grounded, context-aware answers
- **Full-Stack Deployment** — Scalable architecture ready for production
- **Type-Safe APIs** — FastAPI + TypeScript for reliability

## 🏗️ Architecture

```
┌─────────────────┐
│   Next.js UI    │ (Vercel)
│   React + TS    │
└────────┬────────┘
         │ (REST API)
         ↓
┌─────────────────┐
│   FastAPI       │ (DigitalOcean)
│   Backend       │
└────────┬────────┘
         │
         ├─→ [Whisper] → Transcription
         │
         ├─→ [FAISS] → Vector Search
         │
         └─→ [Local LLM] → Response Generation
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** — Modern async Python web framework
- **Whisper** — OpenAI's speech-to-text model
- **LangChain** — LLM orchestration and RAG
- **FAISS** — Facebook's vector similarity search
- **Transformers** — HuggingFace models for embeddings + LLM
- **PostgreSQL** — Transcript and metadata storage

### Frontend
- **Next.js 14** — React + TypeScript full-stack framework
- **Tailwind CSS** — Utility-first styling
- **shadcn/ui** — High-quality component library
- **React Query** — Server state management

### Deployment
- **DigitalOcean** — Backend hosting + GPU support
- **Vercel** — Frontend hosting with CI/CD
- **GitHub Actions** — Automated testing and deployment

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- DigitalOcean account ($200 credit recommended)
- GitHub account
- ~8GB RAM (16GB+ recommended for LLM)

## 🚀 Quick Start

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/transcript-mind.git
cd transcript-mind

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run FastAPI server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📖 Usage

### 1. Transcribe a Video

```bash
curl -X POST "http://localhost:8000/transcribe" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

Response:
```json
{
  "transcript_id": "abc123xyz",
  "transcript": "Full transcript text...",
  "duration_minutes": 45,
  "chunks": 120
}
```

### 2. Ask a Question

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d {
    "transcript_id": "abc123xyz",
    "question": "What are the main takeaways?"
  }
```

Response:
```json
{
  "answer": "The main takeaways are...",
  "sources": [
    "Relevant excerpt from transcript...",
    "Another relevant excerpt..."
  ],
  "confidence": 0.92
}
```

### 3. Via Web UI

Visit `http://localhost:3000`, paste a YouTube URL, and start chatting!

## 📁 Project Structure

```
transcript-mind/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + routes
│   │   ├── models.py            # Pydantic models
│   │   ├── config.py            # Configuration
│   │   └── services/
│   │       ├── transcriber.py    # Whisper integration
│   │       ├── llm_service.py    # LLM inference
│   │       └── rag_service.py    # RAG pipeline
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── pages/
│   │   ├── index.tsx            # Upload page
│   │   └── chat/[id].tsx        # Chat interface
│   ├── components/
│   │   ├── TranscriptUpload.tsx
│   │   └── ChatInterface.tsx
│   ├── services/
│   │   └── api.ts               # API client
│   └── package.json
│
├── .github/
│   └── workflows/
│       ├── backend-deploy.yml
│       └── frontend-deploy.yml
│
└── README.md
```

## 🔄 Workflow

1. **User uploads YouTube URL**
2. **Backend downloads** audio using yt-dlp
3. **Whisper transcribes** audio to text
4. **LangChain chunks** transcript (~300 tokens per chunk)
5. **HuggingFace embeddings** create vectors from chunks
6. **FAISS stores** vectors for fast search
7. **User asks question**
8. **FAISS retrieves** top-5 relevant chunks
9. **Local LLM generates** answer using chunks as context
10. **Frontend displays** answer + source snippets

## 🚢 Deployment

### Backend → DigitalOcean

```bash
# Create Droplet (Ubuntu 22.04, 8GB RAM)
# SSH into droplet and clone repo

# Install Docker
curl https://get.docker.com -sSfL | sh

# Build and run
docker build -t transcript-mind .
docker run -p 8000:8000 transcript-mind
```

### Frontend → Vercel

```bash
# Push to GitHub
git push origin main

# Connect to Vercel via CLI or web dashboard
# Vercel auto-deploys on push
```

### CI/CD with GitHub Actions

See `.github/workflows/` for automated testing and deployment.

## 📊 Performance Metrics

| Operation | Time | GPU | Notes |
|-----------|------|-----|-------|
| Transcribe (1hr video) | ~3-5 min | A100 | Whisper base model |
| Embed transcript | ~2 sec | GPU | FAISS vector creation |
| Search query | <100ms | CPU | FAISS similarity search |
| Generate response | ~2-5 sec | GPU | Mistral-7B inference |

**Total end-to-end:** ~5-10 minutes for transcription, <1 second for chat

## 💰 Cost Analysis

| Service | Monthly | Notes |
|---------|---------|-------|
| DigitalOcean Droplet | $5-6 | Basic tier sufficient |
| Vercel Frontend | $0 | Free tier |
| YouTube API | $0 | Using yt-dlp (free) |
| LLM API | $0 | Local models (free) |
| **Total** | **~$6** | 🎉 Covered by GitHub Student Pack credit |

## 🔐 Privacy & Security

✅ **No external LLM API calls** — Everything runs locally
✅ **No transcripts stored externally** — Kept in your database only
✅ **No telemetry** — Full control over your data
✅ **Rate limiting** — Built-in to prevent abuse

## 🚀 Future Enhancements

- [ ] **User authentication** — NextAuth.js integration
- [ ] **Persistent storage** — Save favorite transcripts + Q&As
- [ ] **Multiple language support** — Multilingual transcription
- [ ] **Advanced RAG** — Hybrid search (semantic + keyword)
- [ ] **Batch processing** — Queue for multiple videos
- [ ] **Export features** — PDF reports, markdown summaries
- [ ] **Web scraping** — Support for podcast websites, blogs

## 📚 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Whisper Model Card](https://huggingface.co/openai/whisper-base)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)
- [FAISS Tutorial](https://github.com/facebookresearch/faiss/wiki/Getting-started)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License — see the LICENSE file for details.

## 👨‍💻 Author

Built by [Your Name] as a portfolio project demonstrating full-stack ML deployment.

**Portfolio highlights:**
- Full-stack development (React + FastAPI)
- ML/AI integration (Whisper, LLMs, RAG)
- Cloud deployment (DigitalOcean, Vercel)
- DevOps practices (Docker, CI/CD, GitHub Actions)

---

**Questions or feedback?** Open an issue or reach out!

⭐ If you find this useful, please consider giving it a star!
