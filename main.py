import os
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException
from huggingface_hub import InferenceClient
from my_lib.transcribe import (
    is_audio_file,
    is_video_file,
    reduce_audio_size,
    extract_audio_from_video
)

app = FastAPI()

# Hugging Face API Key (Replace with your actual key)
HF_API_KEY = "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"

@app.get("/")
async def root():
    return {"message": "Welcome to the Transcription API. Use /transcribe to upload and process files."}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split('.')[-1].lower()
        file_bytes = await file.read()

        if is_audio_file(file.filename):
            processed_audio = reduce_audio_size(file_bytes)
        elif is_video_file(file.filename):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_video:
                temp_video.write(file_bytes)
                temp_video.flush()
                video_path = temp_video.name

            try:
                processed_audio = extract_audio_from_video(video_path)
            finally:
                os.remove(video_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

        # Save processed audio to temporary .wav file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav.write(processed_audio)
            temp_wav.flush()
            temp_wav_path = temp_wav.name

        try:
            client = InferenceClient(provider="fal-ai", api_key=HF_API_KEY)
            output = client.automatic_speech_recognition(temp_wav_path, model="openai/whisper-large-v3")
        finally:
            os.remove(temp_wav_path)

        return {"transcription": output.get("text", "Transcription failed")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# this is a testing comment
