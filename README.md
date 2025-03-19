[![CI](https://github.com/Muhammadyousafrana/audio_transcription/actions/workflows/main.yml/badge.svg)](https://github.com/Muhammadyousafrana/audio_transcription/actions/workflows/main.yml)
# audio_transcription
transcribe the audio into the native language
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/transcribe/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@reduced_audio.wav;type=audio/wav'
```
