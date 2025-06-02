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

async def run_transcription():
    try:
        # DEEPGRAM: Commenting out API key validation
        # if not CONFIG["deepgram_api_key"]:
        #     raise ValueError("DEEPGRAM_API_KEY not found in .env file")
            
        # Ensure video file exists
        if not os.path.exists(CONFIG["video_path"]):
            raise FileNotFoundError(f"Video file not found: {CONFIG['video_path']}")
            
        print(f"Starting transcription for: {CONFIG['video_path']}")
        print(f"Output will be saved to: {CONFIG['output_dir']}")
        
        result = await process_video(
            video_path=CONFIG["video_path"],
            # DEEPGRAM: Commenting out API key
            # deepgram_api_key=CONFIG["deepgram_api_key"],
            whisper_model=CONFIG["whisper_model"],
            output_dir=CONFIG["output_dir"],
            audio_format=CONFIG["audio_format"]
        )
        
        print("\nTranscription completed successfully!")
        print("\nOutput files:")
        print(f"- Audio: {result['output_files']['audio']}")
        print(f"- Whisper transcription: {result['output_files']['whisper']}")
        # DEEPGRAM: Commenting out Deepgram output
        # print(f"- Deepgram transcription: {result['output_files']['deepgram']}")
        
        # Print sample of transcriptions
        print("\nWhisper Transcription (first 100 characters):")
        print(result['whisper']['text'][:100] + "...")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_transcription()) 
