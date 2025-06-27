FROM python:3.10

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential git curl ffmpeg && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Compile Whisper
RUN make && ./models/download-ggml-model.sh base.en

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the Flask server
CMD ["python", "app.py"]
