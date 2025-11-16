# Backend Hosting Guide

## Quick Testing Options

### Option 1: ngrok (Easiest for Quick Testing)

**Setup:**

1. Install ngrok:
```bash
# Download from https://ngrok.com/download
# Or install via package manager:

# macOS
brew install ngrok

# Linux (snap)
sudo snap install ngrok

# Or download directly
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

2. Sign up for free account at https://ngrok.com

3. Authenticate ngrok:
```bash
ngrok authtoken YOUR_TOKEN_HERE
```

4. Start your backend:
```bash
cd transcript-mind/backend
./run.sh
```

5. In a NEW terminal, start ngrok:
```bash
ngrok http 8000
```

6. You'll get a public URL like:
```
https://abc123.ngrok.io
```

7. Test it:
```bash
curl https://abc123.ngrok.io/health
```

**Pros:**
- ✓ Works in minutes
- ✓ Free tier available
- ✓ HTTPS included
- ✓ Great for testing

**Cons:**
- ✗ URL changes each time (unless paid plan)
- ✗ Session expires after inactivity
- ✗ Not for production

---

### Option 2: LocalTunnel (Alternative to ngrok)

**Setup:**

1. Install:
```bash
npm install -g localtunnel
```

2. Start your backend:
```bash
cd transcript-mind/backend
./run.sh
```

3. In new terminal:
```bash
lt --port 8000
```

4. You'll get a URL like:
```
https://funny-turtle-12.loca.lt
```

**Pros:**
- ✓ No signup required
- ✓ Free
- ✓ Simple

**Cons:**
- ✗ Less reliable than ngrok
- ✗ May have IP confirmation page

---

## Cloud Hosting Options

### Option 3: Railway.app (Recommended for Testing/Staging) ⭐

**Cost:** Free tier includes $5/month credit
**Good for:** Semi-permanent testing environment

**Setup:**

1. Install Railway CLI:
```bash
npm install -g @railway/cli
# or
brew install railway
```

2. Login:
```bash
railway login
```

3. From your backend directory:
```bash
cd transcript-mind/backend
railway init
```

4. Create `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Create `runtime.txt`:
```
python-3.11
```

6. Deploy:
```bash
railway up
```

7. Get your URL:
```bash
railway domain
```

**Pros:**
- ✓ Always-on
- ✓ Automatic HTTPS
- ✓ Environment variables
- ✓ Easy deployments
- ✓ Good free tier

**Cons:**
- ✗ Free tier has limits

---

### Option 4: Render.com (Great Free Tier)

**Cost:** Free (with limitations)
**Good for:** Testing/staging environment

**Setup:**

1. Create `render.yaml` in backend directory:
```yaml
services:
  - type: web
    name: transcriptmind-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: YOUTUBE_WHISPER_MODEL
        value: base
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. Push to GitHub

3. Go to https://render.com

4. Connect your GitHub repo

5. Select the backend directory

6. Deploy!

**Pros:**
- ✓ Free tier
- ✓ Auto-deploy from GitHub
- ✓ Always-on
- ✓ HTTPS included

**Cons:**
- ✗ Spins down after 15 mins of inactivity (free tier)
- ✗ Slow cold starts

---

### Option 5: Google Cloud Run (Pay-as-you-go)

**Cost:** Free tier, then pay per request
**Good for:** Production-ready testing

**Setup:**

1. Install Google Cloud CLI

2. Create `Dockerfile` in backend directory:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

3. Deploy:
```bash
gcloud run deploy transcriptmind \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

**Pros:**
- ✓ Scales to zero (save money)
- ✓ Production-grade
- ✓ Fast
- ✓ Generous free tier

**Cons:**
- ✗ More complex setup
- ✗ Cold start delays

---

### Option 6: AWS EC2 (Traditional VPS)

**Cost:** ~$5-10/month (t2.micro/t3.micro)
**Good for:** Full control

**Quick Setup:**

1. Launch Ubuntu EC2 instance

2. SSH into instance

3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv ffmpeg -y
```

4. Clone your repo:
```bash
git clone https://github.com/Kenpachi99/transcript-mind.git
cd transcript-mind/backend
```

5. Run setup:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. Install and configure nginx (reverse proxy)

7. Use systemd to run as service

**Pros:**
- ✓ Full control
- ✓ Always-on
- ✓ Predictable pricing

**Cons:**
- ✗ Need to manage server
- ✗ More complex
- ✗ Need to configure security

---

### Option 7: DigitalOcean App Platform

**Cost:** $5/month minimum
**Good for:** Simple deployment

**Setup:**

1. Push code to GitHub

2. Go to https://cloud.digitalocean.com

3. Create new App

4. Connect GitHub repo

5. Select backend directory

6. Configure:
   - Build command: `pip install -r requirements.txt`
   - Run command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`

7. Deploy!

**Pros:**
- ✓ Simple
- ✓ Always-on
- ✓ Easy scaling

**Cons:**
- ✗ Costs money from day 1

---

## My Recommendation for You

### For Testing Right Now:
**Use ngrok** - it's the fastest way to get a public URL

### For Ongoing Testing/Development:
**Use Railway.app or Render.com** - both have good free tiers

### For Production:
**Use Google Cloud Run or Railway.app** - production-ready with good pricing

---

## Quick Start Script for ngrok

I'll create a helper script for you:

```bash
#!/bin/bash
# File: start_with_ngrok.sh

# Start backend in background
echo "Starting backend..."
cd "$(dirname "$0")"
./run.sh &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Start ngrok
echo "Starting ngrok tunnel..."
ngrok http 8000

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
```

Make it executable:
```bash
chmod +x start_with_ngrok.sh
```

Run it:
```bash
./start_with_ngrok.sh
```

---

## Environment Variables for Cloud Hosting

When deploying to cloud, set these environment variables:

```
YOUTUBE_WHISPER_MODEL=base
PORT=8000  # or $PORT for auto-assigned
DEBUG=false
```

For larger videos, you might need:
```
YOUTUBE_WHISPER_MODEL=tiny  # Smaller, faster, less accurate
```

---

## Next Steps

1. **For quick testing**: Try ngrok first
2. **For sharing with others**: Deploy to Railway or Render
3. **For production**: Use Cloud Run or proper VPS

Need help with any specific option? Let me know!
