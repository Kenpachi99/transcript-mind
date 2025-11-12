"""FastAPI application for YouTube video transcription."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from app.config import settings
from app.services.transcriber import transcriber


# Initialize FastAPI app
app = FastAPI(
    title="TranscriptMind",
    version="0.1.0",
    description="YouTube video transcription service using Whisper AI"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for transcripts (will be replaced with PostgreSQL later)
transcripts_db: Dict[str, Dict[str, Any]] = {}


# Request/Response models
class TranscribeRequest(BaseModel):
    """Request model for transcription endpoint."""
    youtube_url: str


class TranscribeResponse(BaseModel):
    """Response model for transcription endpoint."""
    transcript_id: str
    transcript: str
    language: str
    duration: float
    status: str


# API Endpoints
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Dictionary with service status
    """
    return {
        "status": "healthy",
        "service": "TranscriptMind"
    }


@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_video(request: TranscribeRequest) -> TranscribeResponse:
    """
    Transcribe a YouTube video.

    Args:
        request: Request containing YouTube URL

    Returns:
        TranscribeResponse with transcript and metadata

    Raises:
        HTTPException: If transcription fails or URL is invalid
    """
    try:
        # Validate URL
        if not request.youtube_url:
            raise HTTPException(
                status_code=400,
                detail="YouTube URL required"
            )

        # Perform transcription
        result = transcriber.transcribe(request.youtube_url)

        # Check if transcription was successful
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )

        # Generate unique ID for this transcript
        transcript_id = str(uuid.uuid4())

        # Store transcript in memory
        transcripts_db[transcript_id] = {
            "url": request.youtube_url,
            "transcript": result["transcript"],
            "language": result["language"],
            "duration": result["duration"]
        }

        # Return response
        return TranscribeResponse(
            transcript_id=transcript_id,
            transcript=result["transcript"],
            language=result["language"],
            duration=result["duration"],
            status="success"
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/transcript/{transcript_id}")
async def get_transcript(transcript_id: str) -> Dict[str, Any]:
    """
    Retrieve a previously generated transcript by ID.

    Args:
        transcript_id: UUID of the transcript

    Returns:
        Dictionary containing transcript and metadata

    Raises:
        HTTPException: If transcript not found
    """
    if transcript_id not in transcripts_db:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found"
        )

    return transcripts_db[transcript_id]


# Run the application directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
