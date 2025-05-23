import os
import ffmpeg

def extract_audio_from_video(video_path: str, output_path: str = None, audio_format: str = 'mp3') -> str:
    """
    Extract audio from a video file using ffmpeg-python.
    
    Args:
        video_path (str): Path to the input video file
        output_path (str, optional): Path where the audio file should be saved. 
                                    If not provided, will use the same name as video
                                    with different extension
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

    try:
        # Create an ffmpeg stream
        stream = ffmpeg.input(video_path)
        
        # Extract audio and save it
        stream = ffmpeg.output(stream, output_path, acodec='libmp3lame' if audio_format == 'mp3' else 'pcm_s16le')
        
        # Overwrite if file exists and run the ffmpeg command
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        return output_path
        
    except ffmpeg.Error as e:
        # Clean up the output file if it was created
        if os.path.exists(output_path):
            os.remove(output_path)
        error_message = e.stderr.decode() if e.stderr else str(e)
        raise ffmpeg.Error(f"Error extracting audio: {error_message}")
