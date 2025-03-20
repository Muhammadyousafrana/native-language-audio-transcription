import tempfile
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from huggingface_hub import InferenceClient
from my_lib.transcribe import is_audio_file, is_video_file, reduce_audio_size, extract_audio_from_video

app = FastAPI()

# Hugging Face API Key (Replace with your actual key)
HF_API_KEY = "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"

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the Transcription API. Use /transcribe to upload and process files."}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Endpoint to process and transcribe audio or video files."""
    try:
        file_extension = file.filename.split('.')[-1].lower()

        if is_audio_file(file.filename):
            processed_audio = reduce_audio_size(file.file.read())
        elif is_video_file(file.filename):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_video:
                temp_video.write(file.file.read())
                temp_video.flush()
                video_path = temp_video.name

            try:
                processed_audio = extract_audio_from_video(video_path)
            finally:
                os.remove(video_path)  # Clean up temporary file
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

        # Send processed audio directly to Hugging Face model
        client = InferenceClient(provider="fal-ai", api_key=HF_API_KEY)
        output = client.automatic_speech_recognition(processed_audio, model="openai/whisper-large-v3")

        return {"transcription": output.get("text", "Transcription failed")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
