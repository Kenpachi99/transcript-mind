#!/bin/bash

# TranscriptMind Backend Startup Script

echo "Starting TranscriptMind Backend..."

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
else
    echo ".env file already exists, skipping..."
fi

# Run the FastAPI application
echo "Starting FastAPI server on http://0.0.0.0:8000"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
