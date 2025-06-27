from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['file']
    uid = str(uuid.uuid4())
    os.makedirs('temp', exist_ok=True)
    filepath = f'temp/{uid}.wav'
    output_txt = f'temp/{uid}.txt'

    file.save(filepath)

    # Run whisper.cpp with subprocess
    result = subprocess.run([
        './main', '-m', './models/ggml-base.en.bin',
        '-f', filepath, '-otxt', '-of', f'temp/{uid}'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        return jsonify({'error': 'Transcription failed', 'log': result.stderr.decode()}), 500

    try:
        with open(output_txt, 'r') as f:
            text = f.read()
    except:
        return jsonify({'error': 'Output not found'}), 500

    return jsonify({'text': text})
