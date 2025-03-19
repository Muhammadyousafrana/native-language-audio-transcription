# Use a Python base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory
WORKDIR /app

# Copy the application code and dependencies
COPY main.py /app/
COPY requirements.txt /app/
COPY my_lib /app/my_lib

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

