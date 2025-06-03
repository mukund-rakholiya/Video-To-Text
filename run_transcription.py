from main import process_video
from dotenv.main import load_dotenv
import asyncio
import os

# Load environment variables
load_dotenv() 

# Configuration
CONFIG = {
    "video_path": "videos/demo_tense.mp4",  # Replace with your video path
    "whisper_model": "base",  # Options: tiny, base, small,large, medium 
    "output_dir": "transcriptions",
    "audio_format": "wav"
} 
 
main
async def run_transcription():
    try:
        # Ensure video file exists
        if not os.path.exists(CONFIG["video_path"]):
            raise FileNotFoundError(f"Video file not found: {CONFIG['video_path']}")
            
        print(f"Starting transcription for: {CONFIG['video_path']}")
        print(f"Output will be saved to: {CONFIG['output_dir']}")
        
        result = await process_video(
            video_path=CONFIG["video_path"],
            whisper_model=CONFIG["whisper_model"],
            output_dir=CONFIG["output_dir"],
            audio_format=CONFIG["audio_format"]
        )
        
        print("\nTranscription completed successfully!")
        print("\nOutput files:")
        print(f"- Audio: {result['output_files']['audio']}")
        print(f"- Whisper transcription: {result['output_files']['whisper']}")
        
        # Print sample of transcriptions
        print("\nWhisper Transcription (first 100 characters):")
        print(result['whisper']['text'][:100] + "...")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_transcription()) 
