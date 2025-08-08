from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_handler import generate_explanation # Import the function from gemini_handler.py
import os

app = Flask(__name__)
# Enable CORS for all origins, allowing your frontend to make requests
CORS(app)

@app.route('/')
def home():
    """
    A simple home route to confirm the server is running.
    """
    return "Backend is running! Access /explain for Gemini API integration."

@app.route('/explain', methods=['POST'])
def explain_code():
    """
    API endpoint to receive user input and get an AI explanation from Gemini.
    The AI explanation will be printed to the terminal where the Flask app is running.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_input = data.get('input')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    print(f"\n--- Received User Input for Explanation ---")
    print(user_input)
    print("-------------------------------------------\n")

    # Call the Gemini handler to get the AI explanation
    ai_explanation = generate_explanation(user_input)

    # Print the AI explanation to the terminal (as requested by the user)
    print("\n--- AI Explanation (Printed to Terminal) ---")
    print(ai_explanation)
    print("--------------------------------------------\n")

    # You might also want to send this explanation back to the frontend
    # if you want to display it in the UI, but for now, we're focusing on terminal output.
    return jsonify({"message": "Explanation processed and printed to terminal.", "explanation": ai_explanation})

if __name__ == '__main__':
    # Run the Flask app
    # Set host to '0.0.0.0' to make it accessible from other devices on the network
    # Set debug to True for development, but False for production
    app.run(host='0.0.0.0', port=5000, debug=True)
