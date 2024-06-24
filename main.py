from flask import Flask, request, jsonify, send_file
from tts import tts_full  # Import your TTS function from your_script

app = Flask(__name__)

# Endpoint to handle POST requests for TTS
@app.route('/tts/', methods=['POST'])
def synthesize_text():
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'Invalid request body'}), 400

    text = request.json['text']

    try:
        # Call tts_full to generate the audio file
        tts_full(text)
    except Exception as e:
        return jsonify({'error': f"Error synthesizing text: {str(e)}"}), 500

    # Assuming the file "result_211.wav" is generated successfully
    file_path = "result_211.wav"
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f"Error returning audio file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001)  # Use a different port, e.g., 8001

