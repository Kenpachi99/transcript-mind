#!/bin/bash

# Helper script to start backend with ngrok tunnel
# This allows you to test your backend from anywhere with a public URL

echo "========================================="
echo "  TranscriptMind - ngrok Quick Start"
echo "========================================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed!"
    echo ""
    echo "Install it with:"
    echo "  macOS:  brew install ngrok"
    echo "  Linux:  sudo snap install ngrok"
    echo "  Or download from: https://ngrok.com/download"
    echo ""
    echo "After installing, sign up at https://ngrok.com and run:"
    echo "  ngrok authtoken YOUR_TOKEN"
    exit 1
fi

echo "✓ ngrok found"
echo ""

# Start backend in background
echo "Starting backend server..."
./run.sh &
BACKEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM EXIT

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 8

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Backend is running on http://localhost:8000"
    echo ""
else
    echo "❌ Backend failed to start"
    echo "Check the output above for errors"
    exit 1
fi

# Start ngrok
echo "========================================="
echo "Starting ngrok tunnel..."
echo "========================================="
echo ""
echo "Your public URL will appear below:"
echo "Press Ctrl+C to stop"
echo ""

ngrok http 8000
