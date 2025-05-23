import os
import ffmpeg

def extract_audio_from_video(video_path: str, output_path: str = None, audio_format: str = 'mp3') -> str:
    """
    Extract audio from a video file using ffmpeg-python.
    
    Args:
        video_path (str): Path to the input video file
        output_path (str, optional): Path where the audio file should be saved. 
                                    If not provided, will use the same name as video with different extension
        audio_format (str, optional): Format of the output audio file. Defaults to 'mp3'
    
    Returns:
        str: Path to the extracted audio file
        
    Raises:
        FileNotFoundError: If the input video file doesn't exist
        ffmpeg.Error: If there's an error during audio extraction
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # If output path is not provided, create one based on input video path
    if output_path is None:
        output_path = os.path.splitext(video_path)[0] + f'.{audio_format}'