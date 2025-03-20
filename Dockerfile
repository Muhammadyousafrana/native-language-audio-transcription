# Use a Python base image with FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory
WORKDIR /app

# Install system dependencies (FFmpeg)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the application code and dependencies
COPY main.py /app/
COPY requirements.txt /app/
COPY my_lib /app/my_lib

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt