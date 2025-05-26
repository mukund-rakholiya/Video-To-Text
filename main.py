import asyncio
from pathlib import Path
# DEEPGRAM: Commenting out Deepgram import
# from transcribers import transcribe_audio, transcribe_audio_deepgram
from transcribers import transcribe_audio
from utils import extract_audio_from_video
import os
from dotenv.main import load_dotenv