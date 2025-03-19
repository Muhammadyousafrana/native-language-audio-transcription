import io
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
        # Load audio from bytes
        audio_io = io.BytesIO(audio_bytes)
        y, sr = librosa.load(audio_io, sr=None)

        # Downsample to target sample rate and convert to mono
        y_resampled = librosa.core.resample(y, orig_sr=sr, target_sr=target_sr)
        y_mono = librosa.to_mono(y_resampled)

        # Save to in-memory file
        output_io = io.BytesIO()
        sf.write(output_io, y_mono, target_sr, format='wav', subtype='PCM_16')
        output_io.seek(0)

        return output_io.read()

    except Exception as e:
        raise RuntimeError(f"Error processing audio: {e}") from e

def extract_audio_from_video(video_path: str, target_sr: int = 16000) -> bytes:
    """Extracts audio from a video file, reduces its size, and returns it as bytes."""
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio:
            # Extract audio using FFmpeg
            command = [
                "ffmpeg",
                "-i", video_path,
                "-vn",  # Disable video
                "-acodec", "pcm_s16le",
                "-ar", str(target_sr),
                "-ac", "1",
                temp_audio.name
            ]
            subprocess.run(command, check=True)

            # Read and process audio file
            temp_audio.seek(0)
            audio_bytes = temp_audio.read()

            return reduce_audio_size(audio_bytes, target_sr)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e}") from e

    except Exception as e:
        raise RuntimeError(f"Error processing video: {e}") from e
