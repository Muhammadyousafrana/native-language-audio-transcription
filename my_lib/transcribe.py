import io
import os
import tempfile
import subprocess
import librosa
import soundfile as sf

def is_audio_file(file_path: str) -> bool:
    """Check if the file is an audio file based on its extension."""
    audio_extensions = ('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a')
    return file_path.lower().endswith(audio_extensions)

def is_video_file(file_path: str) -> bool:
    """Check if the file is a video file based on its extension."""
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm')
    return file_path.lower().endswith(video_extensions)

def reduce_audio_size(audio_bytes: bytes, target_sr: int = 16000) -> bytes:
    """Reduces the size of an audio file and returns it as bytes."""
    try:
        audio_io = io.BytesIO(audio_bytes)
        y, sr = librosa.load(audio_io, sr=None)

        # Downsample and convert to mono
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr, res_type='kaiser_fast')
        y_mono = librosa.to_mono(y_resampled)

        # Save to in-memory file
        output_io = io.BytesIO()
        sf.write(output_io, y_mono, target_sr, format='wav', subtype='PCM_16')
        output_io.seek(0)

        return output_io.read()
    except Exception as e:
        raise RuntimeError(f"Error processing audio: {e}")

def extract_audio_from_video(video_path: str, target_sr: int = 16000) -> bytes:
    """Extracts and processes audio from a video file using FFmpeg."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            temp_audio_path = temp_audio_file.name

        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", str(target_sr),
            "-ac", "1",
            "-y",  # Force overwrite
            temp_audio_path
        ]

        subprocess.run(command, capture_output=True, text=True, check=True)

        with open(temp_audio_path, "rb") as f:
            audio_bytes = f.read()

        os.remove(temp_audio_path)  # Clean up
        return reduce_audio_size(audio_bytes, target_sr)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr}")
    except Exception as e:
        raise RuntimeError(f"Error processing video: {e}")