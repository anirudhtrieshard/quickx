#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = '/var/www/quickx/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = None  # No file size limit

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            # Secure the filename to prevent directory traversal attacks
            filename = secure_filename(file.filename)

            # If filename becomes empty after securing (e.g., only special chars), use a default
            if not filename:
                filename = 'unnamed_file'

            # Save the file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # If file exists, append a number
            counter = 1
            base_name, extension = os.path.splitext(filename)
            while os.path.exists(filepath):
                filename = f"{base_name}_{counter}{extension}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                counter += 1

            file.save(filepath)

            # Set permissions so www-data can read it
            os.chmod(filepath, 0o644)

            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename
            }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Run on localhost only, nginx will proxy to this
    app.run(host='127.0.0.1', port=5000, debug=False)
