"""YouTube video transcription service using Whisper."""
import os
import subprocess
import whisper
from pathlib import Path
from typing import Dict, Any


class YouTubeTranscriber:
    """Service for downloading and transcribing YouTube videos."""

    def __init__(self, model_name: str = "base"):
        """
        Initialize the transcriber.

        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self.model = None
        self.temp_dir = Path("./temp_audio")
        self.temp_dir.mkdir(exist_ok=True)

    def load_model(self) -> whisper.Whisper:
        """
        Load the Whisper model lazily.

        Returns:
            Loaded Whisper model instance
        """
        if self.model is None:
            print(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
        return self.model

    def download_audio(self, youtube_url: str) -> str:
        """
        Download audio from YouTube URL using yt-dlp.

        Args:
            youtube_url: URL of the YouTube video

        Returns:
            Path to the downloaded audio file

        Raises:
            Exception: If download fails or no audio file is found
        """
        output_template = str(self.temp_dir / "audio")
        command = [
            'yt-dlp',
            '-f', 'bestaudio',
            '-x',
            '--audio-format', 'mp3',
            '-o', output_template,
            youtube_url
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Download failed: {result.stderr}")

            # Find the downloaded file
            audio_files = list(self.temp_dir.glob("audio.*"))
            if not audio_files:
                raise Exception("No audio file found after download")

            return str(audio_files[0])
        except Exception as e:
            raise Exception(f"Error downloading audio: {str(e)}")

    def transcribe(self, youtube_url: str) -> Dict[str, Any]:
        """
        Download and transcribe a YouTube video.

        Args:
            youtube_url: URL of the YouTube video to transcribe

        Returns:
            Dictionary containing:
                - success (bool): Whether transcription was successful
                - transcript (str): The transcribed text (if successful)
                - language (str): Detected language
                - duration (float): Video duration in seconds
                - error (str): Error message (if failed)
        """
        try:
            # Load model
            model = self.load_model()

            # Download audio
            print(f"Downloading audio from: {youtube_url}")
            audio_path = self.download_audio(youtube_url)
            print(f"Audio saved to: {audio_path}")

            # Transcribe
            print("Starting transcription...")
            result = model.transcribe(audio_path, language="en")

            # Extract transcript
            transcript = result["text"]

            # Cleanup downloaded file
            os.remove(audio_path)

            return {
                "success": True,
                "transcript": transcript,
                "language": result.get("language", "en"),
                "duration": result.get("duration", 0)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global transcriber instance
transcriber = YouTubeTranscriber()
