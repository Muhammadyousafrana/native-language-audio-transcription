import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from huggingface_hub import InferenceClient
from my_lib.transcribe import is_audio_file, is_video_file, reduce_audio_size, extract_audio_from_video

app = FastAPI()

# Hugging Face API Key (Replace with your actual key)
HF_API_KEY = "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"

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    """Endpoint to process and transcribe audio or video files."""
    try:
        file_bytes = await file.read()
        file_extension = file.filename.split('.')[-1].lower()

        if is_audio_file(file.filename):
            processed_audio = reduce_audio_size(file_bytes)
        elif is_video_file(file.filename):
            # Save the uploaded video file temporarily
            temp_video_path = f"temp_video.{file_extension}"
            with open(temp_video_path, "wb") as f:
                f.write(file_bytes)

            processed_audio = extract_audio_from_video(temp_video_path)
            os.remove(temp_video_path)  # Remove temporary file
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Send processed audio directly to Hugging Face model
        client = InferenceClient(provider="fal-ai", api_key=HF_API_KEY)
        output = client.automatic_speech_recognition(processed_audio, model="openai/whisper-large-v3")

        return {"transcription": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
