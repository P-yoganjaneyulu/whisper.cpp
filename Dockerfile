FROM python:3.10

# 🔧 Install system dependencies: build tools, ffmpeg, curl, cmake
RUN apt-get update && \
    apt-get install -y build-essential git curl ffmpeg cmake && \
    apt-get clean

# 📁 Set working directory
WORKDIR /app

# 📦 Copy all app files into container
COPY . .

# 🧱 Build Whisper.cpp
RUN make && ./models/download-ggml-model.sh base.en

# 🐍 Install Python dependencies
RUN pip install -r requirements.txt

# 🚀 Run the Flask app
CMD ["python", "app.py"]
