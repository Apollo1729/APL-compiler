// gemini.ts
// This file handles the communication with your Python backend.

const API_BASE_URL = 'http://localhost:5000'; // Make sure this matches your Flask app's address

/**
 * Sends a request to the backend to get an AI explanation for the given input.
 * @param input The text or code snippet to be explained.
 * @returns A Promise that resolves with the AI explanation message or an error.
 */
export async function getGeminiExplanation(input: string): Promise<string> {
    try {
        const response = await fetch(`${API_BASE_URL}/explain`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: input }),
        });

        if (!response.ok) {
            // If the response is not OK (e.g., 400, 500), throw an error
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        // The backend prints to the terminal, but we can still return the message
        // or the explanation if the backend sends it back.
        return data.message || data.explanation || "Explanation request sent successfully.";
    } catch (error: any) {
        console.error("Error sending request to backend:", error);
        return `Failed to get explanation: ${error.message}`;
    }
}