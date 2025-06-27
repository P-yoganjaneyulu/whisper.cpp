from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No audio file found in request'}), 400

    file = request.files['file']
    uid = str(uuid.uuid4())
    os.makedirs('temp', exist_ok=True)
    
    input_path = f'temp/{uid}.wav'
    output_path = f'temp/{uid}.txt'

    # Save the uploaded audio
    file.save(input_path)

    # Run whisper.cpp via subprocess
    result = subprocess.run([
        './main', '-m', './models/ggml-base.en.bin',
        '-f', input_path, '-otxt', '-of', f'temp/{uid}'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check for errors in transcription
    if result.returncode != 0:
        return jsonify({
            'error': 'Transcription failed',
            'stderr': result.stderr.decode()
        }), 500

    # Read transcribed output
    try:
        with open(output_path, 'r') as f:
            text = f.read().strip()
    except FileNotFoundError:
        return jsonify({'error': 'Output file not found'}), 500

    # Return transcription result
    return jsonify({'text': text})

@app.route('/', methods=['GET'])
def health_check():
    return "🟢 Whisper API is running", 200

# Make it listen publicly on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

