# TranscriptMind Backend - Testing Guide

## Quick Start

### 1. Setup Environment

First, navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment (if not already created):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

You can edit `.env` to change the Whisper model (tiny, base, small, medium, large):
```
YOUTUBE_WHISPER_MODEL=base
```

### 4. Run the Server

**Option A: Using the startup script (recommended)**
```bash
./run.sh
```

**Option B: Manual startup**
```bash
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

---

## Testing the API

### View Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces let you test all endpoints directly in your browser!

---

## API Endpoints

### 1. Health Check

**Test if the server is running:**

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "TranscriptMind"
}
```

---

### 2. Transcribe YouTube Video

**Basic curl command:**
```bash
curl -X POST http://localhost:8000/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }'
```

**Expected Response:**
```json
{
  "transcript_id": "550e8400-e29b-41d4-a716-446655440000",
  "transcript": "Full transcription text here...",
  "language": "en",
  "duration": 212.5,
  "status": "success"
}
```

**Test with a short video (recommended for testing):**
```bash
curl -X POST http://localhost:8000/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"
  }'
```
*(This is the "Me at the zoo" video - first YouTube video, only 19 seconds)*

---

### 3. Retrieve Transcript by ID

After transcribing, use the `transcript_id` to retrieve it:

```bash
curl http://localhost:8000/transcript/YOUR_TRANSCRIPT_ID_HERE
```

**Expected Response:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "transcript": "Full transcription text...",
  "language": "en",
  "duration": 212.5
}
```

---

## Testing with Python

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Health check
print("Testing health check...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# 2. Transcribe a short video
print("Testing transcription...")
youtube_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
response = requests.post(
    f"{BASE_URL}/transcribe",
    json={"youtube_url": youtube_url}
)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Transcript ID: {data.get('transcript_id')}")
print(f"Transcript: {data.get('transcript')[:100]}...")
print(f"Language: {data.get('language')}")
print(f"Duration: {data.get('duration')} seconds\n")

# 3. Retrieve transcript
transcript_id = data.get('transcript_id')
print(f"Retrieving transcript {transcript_id}...")
response = requests.get(f"{BASE_URL}/transcript/{transcript_id}")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")
```

Run it:
```bash
python test_api.py
```

---

## Testing with HTTPie (if installed)

HTTPie provides a more readable CLI for API testing:

```bash
# Install HTTPie
pip install httpie

# Health check
http GET localhost:8000/health

# Transcribe
http POST localhost:8000/transcribe youtube_url="https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Get transcript
http GET localhost:8000/transcript/TRANSCRIPT_ID
```

---

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use: `lsof -i :8000`
- Try a different port: `uvicorn app.main:app --port 8001`

### Dependencies fail to install
- Make sure you're using Python 3.8+: `python3 --version`
- Install system dependencies for yt-dlp: `sudo apt-get install ffmpeg` (Linux)

### Transcription fails
- Check if yt-dlp can download the video: `yt-dlp --get-title YOUR_URL`
- Try a shorter video for testing
- Check the Whisper model is downloaded (happens automatically on first use)

### Out of memory
- Use a smaller Whisper model in `.env`: `YOUTUBE_WHISPER_MODEL=tiny`
- Models: tiny (39MB) < base (74MB) < small (244MB) < medium (769MB) < large (1550MB)

---

## Development Tips

### Watch Logs
The server runs with `--reload` flag, so it will automatically restart when you make code changes.

### Check Downloaded Audio
Audio files are temporarily stored in `temp_audio/` directory and deleted after transcription.

### Debug Mode
Set `debug: True` in `app/config.py` for detailed error messages.

---

## Next Steps

- Add PostgreSQL database for persistent storage
- Add authentication/API keys
- Add rate limiting
- Add job queue for async processing
- Add support for multiple languages
- Add subtitle file export (SRT, VTT)
