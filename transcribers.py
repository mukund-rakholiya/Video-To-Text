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

async def transcribe_audio_deepgram(
    audio_path: Union[str, Path],
    api_key: str,
    language: str = "en",
    model: str = "general",
    tier: str = "enhanced",
    smart_format: bool = True,
    diarize: bool = False,
    punctuate: bool = True
) -> Dict:
    """
    Transcribe audio using Deepgram's API with async support.
    
    Args:
        audio_path (Union[str, Path]): Path to the audio file
        api_key (str): Deepgram API key
        language (str): Language code (e.g., 'en' for English)
        model (str): Model to use (e.g., 'general', 'meeting', 'phonecall')
        tier (str): Processing tier ('enhanced' or 'base')
        smart_format (bool): Whether to enable smart formatting
        diarize (bool): Whether to enable speaker diarization
        punctuate (bool): Whether to add punctuation
        
    Returns:
        Dict: Dictionary containing transcription results including:
            - text: Full transcription text
            - words: List of words with timestamps
            - confidence: Overall confidence score
            - speakers: Speaker diarization (if enabled)
    """

    # Convert string path to Path object if necessary
    audio_path = Path(audio_path) if isinstance(audio_path, str) else audio_path
    
    # Validate audio file exists
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Initialize Deepgram client
    deepgram = Deepgram(api_key)
    
    # Prepare audio file
    with open(str(audio_path), 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        
        # Configure transcription options
        options = {
            'smart_format': smart_format,
            'model': model,
            'language': language,
            'tier': tier,
            'punctuate': punctuate
        }
        
        if diarize:
            options['diarize'] = True
        
        # Perform transcription
        response = await deepgram.transcription.prerecorded(source, options)
        
        # Extract results
        result = response['results']
        channels = result['channels'][0]  # Get first channel
        alternatives = channels['alternatives'][0]  # Get first alternative
        
        # Prepare return dictionary
        transcription_result = {
            'text': alternatives.get('transcript', ''),
            'confidence': alternatives.get('confidence', 0),
            'words': alternatives.get('words', []),
            'language': result.get('language', language)
        }
        
        # Add speaker diarization if enabled
        if diarize and 'speaker_labels' in alternatives:
            transcription_result['speakers'] = alternatives['speaker_labels']
        
        return transcription_result
