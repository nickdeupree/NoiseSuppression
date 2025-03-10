/**
 * Audio processing service for noise suppression
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

/**
 * Process an audio file to remove background noise
 * 
 * @param {File} audioFile - The audio file to process
 * @returns {Promise<Blob>} - The processed audio file as a blob
 */
interface ProcessAudioResponse {
    error?: string;
}

export async function processAudio(audioFile: File): Promise<Blob> {
    if (!audioFile) {
        throw new Error('No audio file provided');
    }
    
    const formData = new FormData();
    formData.append('file', audioFile);
    
    try {
        const response = await fetch(`${API_URL}/process-audio`, {
            method: 'POST',
            body: formData,
        });
        
        if (!response.ok) {
            const errorData: ProcessAudioResponse = await response.json();
            throw new Error(errorData.error || 'Failed to process audio');
        }
        
        return await response.blob();
    } catch (error) {
        console.error('Error processing audio:', error);
        throw error;
    }
}

/**
 * Get available noise reduction models
 * 
 * @returns {Promise<Array>} - List of available models
 */
export async function getAvailableModels() {
  try {
    const response = await fetch(`${API_URL}/available-models`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch available models');
    }
    
    const data = await response.json();
    return data.models || [];
  } catch (error) {
    console.error('Error fetching models:', error);
    throw error;
  }
}