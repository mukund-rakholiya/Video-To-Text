import whisper
from typing import Dict, Optional, Union
from pathlib import Path
import asyncio
from deepgram import Deepgram

def transcribe_audio(
    audio_path: Union[str, Path],
    model_name: str = "base",
    language: Optional[str] = None,
    task: str = "transcribe",
    verbose: bool = False
) -> Dict:
    """
    Transcribe audio using OpenAI's Whisper model.
    
    Args:
        audio_path (Union[str, Path]): Path to the audio file
        model_name (str): Whisper model to use (tiny, base, small, medium, large)
        language (Optional[str]): Language code (e.g., 'en' for English). If None, auto-detect
        task (str): Either 'transcribe' or 'translate' (translate to English)
        verbose (bool): Whether to show progress
        
    Returns:
        Dict: Dictionary containing transcription results including:
            - text: Full transcription text
            - segments: List of transcribed segments with timestamps
            - language: Detected or specified language
    """
