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

    try:
        # Convert string path to Path object if necessary
        audio_path = Path(audio_path) if isinstance(audio_path, str) else audio_path
        
        # Validate audio file exists
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        # Load the Whisper model
        if verbose:
            print(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        
        # Prepare transcription options
        options = {
            "task": task,
            "verbose": verbose
        }
        if language:
            options["language"] = language
            
        # Perform transcription
        if verbose:
            print("Starting transcription...")
        result = model.transcribe(str(audio_path), **options)
        
        return {
            "text": result["text"],
            "segments": result["segments"],
            "language": result["language"]
        }
        
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")
