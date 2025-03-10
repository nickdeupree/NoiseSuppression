import os
import tensorflow as tf
from flask import Blueprint, request, jsonify, send_file
import uuid
from audio_processing.noise_reduction import predict_tflite

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@api_bp.route('/process-audio', methods=['POST'])
def process_audio():
    """Endpoint to process audio file and remove background noise"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Create temporary directories if they don't exist
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate unique filenames
    input_filename = f"{uuid.uuid4()}.wav"
    output_filename = f"{uuid.uuid4()}.wav"
    
    input_path = os.path.join(temp_dir, input_filename)
    output_path = os.path.join(temp_dir, output_filename)
    
    try:
        # Save the input file
        file.save(input_path)
        
        # Process the audio
        processed_audio, sample_rate = predict_tflite(input_path)
        
        # Save the processed audio (ensure sample_rate is an integer)
        tf.io.write_file(
            output_path,
            tf.audio.encode_wav(processed_audio, sample_rate=int(sample_rate))  # Convert to int here
        )
        
        return send_file(output_path, as_attachment=True, download_name="processed_audio.wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temp files
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as e:
            print(f"Error cleaning up temporary files: {e}")