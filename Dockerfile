# Use the AWS Lambda Python base image
#FROM public.ecr.aws/lambda/python:3.12
FROM python:3.10
# Set the working directory to /app
WORKDIR /app

# Copy the application code and dependencies
COPY main.py /app/
COPY requirements.txt /app/
COPY my_lib /app/my_lib

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI default port
EXPOSE 8080

# Command to run the FastAPI app

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]