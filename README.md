# Audio Noise Suppression

A web application that leverages machine learning to remove background noise from audio files.

## Overview

This project combines a Next.js frontend with a Python Flask backend to provide an easy-to-use interface for audio noise suppression. The system uses a TensorFlow-based deep learning model to process audio files and remove unwanted background noise, providing cleaner audio output.

## Features

- Upload audio files through a user-friendly interface
- Real-time processing of audio files with noise suppression
- Preview of both original and processed audio
- Download capability for processed audio files
- Responsive design that works across devices

## Architecture

### Frontend (Next.js)
- Built with Next.js and React
- Uses HeroUI component library for UI elements
- Responsive design with gradient background
- Audio upload, preview, and download functionality

### Backend (Flask)
- RESTful API built with Flask
- TensorFlow/TFLite for audio processing
- Handles file uploads, processing, and serving processed files
- Implements a U-Net style convolutional neural network for noise reduction

## Tech Stack

- **Frontend**:
  - Next.js / React
  - TypeScript
  - HeroUI components
  - Audio Web API

- **Backend**:
  - Python 3.11+
  - Flask & Flask-CORS
  - TensorFlow 2.18
  - Librosa (audio processing)

- **Machine Learning**:
  - TensorFlow/Keras for model training
  - TFLite for optimized inference
  - Convolutional neural network architecture

## Getting Started

### Prerequisites

- Node.js (v14+)
- Python 3.11+
- pip
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/audio-noise-suppression.git
   cd audio-noise-suppression
   ```

2. **Set up the frontend**
   ```bash
   # Install dependencies
   npm install
   # or
   yarn install
   ```

3. **Set up the backend**
   ```bash
   # Create a virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   cd python
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd python
   python main.py
   ```
   This will start the Flask API server on http://localhost:5000

2. **Start the frontend development server**
   ```bash
   # From the project root
   npm run dev
   # or
   yarn dev
   ```
   This will start the Next.js development server on http://localhost:3000

3. **Access the application**
   
   Open your browser and navigate to http://localhost:3000

## Usage

1. Open the application in your browser
2. Click on the "Upload Audio" button to select an audio file
3. After uploading, click "Process Audio" to remove background noise
4. Once processing is complete, you can:
   - Listen to both the original and processed audio
   - Download the processed audio file

## Deployment

### Frontend (Next.js)

The Next.js application can be deployed to Vercel, Netlify, or any other Next.js-compatible hosting platform:

```bash
# Build the application
npm run build
# or
yarn build

# Start in production mode
npm start
# or
yarn start
```

### Backend (Flask)

The Flask backend can be deployed to platforms like Heroku, AWS, Google Cloud, or any other Python-compatible hosting service:

```bash
# Set the PORT environment variable if needed
export PORT=8080

# Start the server
python python/main.py
```