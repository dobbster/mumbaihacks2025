/**
 * API service for communicating with the backend LangGraph server
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:2024';

/**
 * Call the verify endpoint to check misinformation
 * @param {string} prompt - The user's query/question
 * @param {number} maxResults - Maximum number of results (optional)
 * @returns {Promise<Object>} Classification results
 */
export async function verifyMisinformation(prompt, maxResults = 5) {
  try {
    const response = await fetch(`${API_BASE_URL}/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: prompt,
        max_results: maxResults,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error calling verify endpoint:', error);
    throw error;
  }
}

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
}

