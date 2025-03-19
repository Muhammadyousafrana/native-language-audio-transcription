# Use a Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the application code and dependencies
COPY main.py /app/
COPY requirements.txt /app/
COPY my_lib /app/my_lib

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Heroku dynamic port (Not needed, but for reference)
EXPOSE 8080

# Default command for Heroku, using the dynamic port
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:${PORT}"]
