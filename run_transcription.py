import asyncio
from main import process_video
import os
from dotenv.main import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CONFIG = {
    "video_path": "videos/demo_tense.mp4",  # Replace with your video path
    # DEEPGRAM: Commenting out API key
    # "deepgram_api_key": os.getenv("DEEPGRAM_API_KEY"),  # Get API key from .env
    "whisper_model": "base",  # Options: tiny, base, small, medium, large
    "output_dir": "transcriptions",
    "audio_format": "wav"
}