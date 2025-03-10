import tensorflow as tf
import numpy as np
import os
import librosa

# Match the same batching size used during training
BATCHING_SIZE = 12000
MODEL_SAMPLE_RATE = 16000

def resample_if_necessary(audio, orig_sample_rate):
    """Resample audio to the model's expected sample rate if needed"""
    # Convert sample rate to integer
    orig_sample_rate = int(orig_sample_rate)  # Add this line
    
    if orig_sample_rate != MODEL_SAMPLE_RATE:
        # Use librosa for high-quality resampling
        audio_np = np.squeeze(audio.numpy())
        resampled_audio = librosa.resample(
            y=audio_np, 
            orig_sr=orig_sample_rate, 
            target_sr=MODEL_SAMPLE_RATE
        )
        return tf.convert_to_tensor(resampled_audio[:, np.newaxis], dtype=tf.float32), MODEL_SAMPLE_RATE
    return audio, orig_sample_rate

def get_audio(path):
    """Load an audio file and get its sample rate"""
    audio_file = tf.io.read_file(path)
    audio, sample_rate = tf.audio.decode_wav(audio_file, desired_channels=1)
    
    # Resample to match the model's expected sample rate
    audio, sample_rate = resample_if_necessary(audio, sample_rate)
    
    return audio, sample_rate

def ensure_model_loaded():
    """Get path to the model file and ensure it exists"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # First try the TFLite model
    model_path = os.path.join(project_root, 'python', 'models', 'TFLiteModel.tflite')
    
    # If TFLite model doesn't exist, try the Keras model
    if not os.path.exists(model_path):
        keras_path = os.path.join(project_root, 'python', 'models', 'NoiseSuppressionModel.keras')
        if os.path.exists(keras_path):
            # Convert Keras model to TFLite
            convert_keras_to_tflite(keras_path, model_path)
        else:
            raise FileNotFoundError(f"No model found at {model_path} or {keras_path}")
    
    return model_path

def convert_keras_to_tflite(keras_path, tflite_path):
    """Convert Keras model to TFLite format"""
    print(f"Converting Keras model {keras_path} to TFLite...")
    model = tf.keras.models.load_model(keras_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    # Save the model
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
    print(f"TFLite model saved to {tflite_path}")

def process_in_batches(audio):
    """Process audio in batches of size BATCHING_SIZE as done during training"""
    audio_len = audio.shape[0]
    batches = []
    
    # Process complete batches
    for i in range(0, audio_len, BATCHING_SIZE):
        if i + BATCHING_SIZE <= audio_len:
            batches.append(audio[i:i + BATCHING_SIZE])
        else:
            # For the last incomplete batch, pad with zeros
            last_batch = audio[i:]
            padding_size = BATCHING_SIZE - last_batch.shape[0]
            padded = tf.pad(last_batch, [[0, padding_size], [0, 0]])
            batches.append(padded)
    
    return tf.stack(batches), audio_len

def predict_tflite(path):
    """Process audio using the TFLite model with proper batching"""
    # Get the model path and initialize interpreter
    model_path = ensure_model_loaded()
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    # Load and process audio
    audio, orig_sample_rate = get_audio(path)
    batched_audio, orig_length = process_in_batches(audio)
    
    # Get input and output details
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    
    # Process each batch
    processed_batches = []
    for batch in batched_audio:
        interpreter.set_tensor(input_details['index'], tf.expand_dims(batch, 0))
        interpreter.invoke()
        processed_batch = interpreter.get_tensor(output_details['index'])
        processed_batches.append(processed_batch[0])
    
    # Reconstruct the full audio
    processed_audio = tf.concat(processed_batches, axis=0)
    
    # Trim to original length
    processed_audio = processed_audio[:orig_length]
    
    # If we resampled, we need to resample back to original rate
    if orig_sample_rate != MODEL_SAMPLE_RATE:
        processed_np = np.squeeze(processed_audio.numpy())
        processed_np = librosa.resample(
            y=processed_np,
            orig_sr=MODEL_SAMPLE_RATE,
            target_sr=orig_sample_rate
        )
        processed_audio = tf.convert_to_tensor(processed_np[:, np.newaxis], dtype=tf.float32)
    
    # Make sure sample_rate is an integer
    return processed_audio, int(orig_sample_rate)  # Convert to int here