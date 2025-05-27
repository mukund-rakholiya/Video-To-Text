import asyncio
from pathlib import Path
# DEEPGRAM: Commenting out Deepgram import
# from transcribers import transcribe_audio, transcribe_audio_deepgram
from transcribers import transcribe_audio
from utils import extract_audio_from_video
import os
from dotenv.main import load_dotenv

# Load environment variables
load_dotenv()

async def process_video(
    video_path: str,
    deepgram_api_key: str = None,  # DEEPGRAM: Kept for future use
    whisper_model: str = "base",
    output_dir: str = "transcriptions",
    audio_format: str = "wav"
) -> dict:
    """
    Process a video file by extracting audio and transcribing with Whisper.
    
    Args:
        video_path (str): Path to the video file
        deepgram_api_key (str): Deepgram API key (optional if set in .env) # DEEPGRAM: Kept for documentation
        whisper_model (str): Whisper model to use
        output_dir (str): Directory to save transcriptions
        audio_format (str): Format for extracted audio (wav or mp3)
        
    Returns:
        dict: Dictionary containing transcriptions
    """
        # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Extract audio from video using ffmpeg
    print("Extracting audio from video...")
    video_name = Path(video_path).stem
    audio_path = str(output_path / f"{video_name}.{audio_format}")
    extracted_audio = extract_audio_from_video(
        video_path=video_path,
        output_path=audio_path,
        audio_format=audio_format
    )
    
    print("Starting transcription process...")

    # Run Whisper transcription
    whisper_result = transcribe_audio(
        extracted_audio,
        model_name=whisper_model,
        verbose=True
    )

    # Save transcriptions to files
    whisper_output = output_path / f"{video_name}_whisper.txt"
    with open(whisper_output, 'w', encoding='utf-8') as f:
        f.write(whisper_result['text'])

    # Clean up extracted audio if it's not in the output directory
    if not str(extracted_audio).startswith(str(output_path)):
        os.unlink(extracted_audio)

    return {
        'whisper': whisper_result,
        # DEEPGRAM: Commenting out Deepgram result
        # 'deepgram': deepgram_result,
        'output_files': {
            'audio': str(extracted_audio),
            'whisper': str(whisper_output),
            # DEEPGRAM: Commenting out Deepgram output
            # 'deepgram': str(deepgram_output)
        }
    }
