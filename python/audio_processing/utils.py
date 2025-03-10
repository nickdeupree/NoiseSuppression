import os
import tensorflow as tf
import numpy as np
import librosa
import soundfile as sf

def load_audio(file_path, target_sr=16000):
    """
    Load an audio file with librosa and optionally resample it
    """
    audio, sr = librosa.load(file_path, sr=None)
    
    # Resample if needed
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
        
    return audio, sr

def save_audio(audio, file_path, sr=16000):
    """
    Save audio to file
    """
    sf.write(file_path, audio, sr)
    
def wav_to_float32(audio_path):
    """
    Convert a WAV file to float32 tensor
    """
    audio, _ = tf.audio.decode_wav(tf.io.read_file(audio_path), desired_channels=1)
    return tf.cast(audio, tf.float32)

def ensure_model_loaded():
    """
    Ensure the TFLite model is properly loaded
    """
    model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'TFLiteModel.tflite')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    return model_path