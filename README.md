# Native Language Audio Transcription

Transcribe audio into the user's native language and expose it through a simple API.

## Overview

This project provides a lightweight service for taking uploaded audio files and converting the spoken content into text in the target language. It is designed to be easy to run locally and quick to integrate into an application workflow.

## API example

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/transcribe/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@reduced_audio.wav;type=audio/wav'
```

## Suggested repository name

A more descriptive repository name would be:

`native-language-audio-transcription`

This more clearly reflects the purpose of the project than `audio_transcription`.
