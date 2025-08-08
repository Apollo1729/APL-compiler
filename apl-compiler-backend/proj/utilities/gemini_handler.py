import os
from google.genai import types
from google import genai
from dotenv import load_dotenv
import aiofiles  # async file operations
from pathlib import Path
import json


class Gemini_Handler:

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Configure the Gemini API with your API key
        # The API key is loaded from the environment variable GEMINI_API_KEY
        try:
            self.API_KEY = os.getenv("GEMINI_API_KEY")
            print(f"Using Gemini API Key: {self.API_KEY}")  # Debugging line to check if API key is loaded
            if not self.API_KEY:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")
            # genai.configure(api_key=API_KEY)
            self.client = genai.Client(api_key=self.API_KEY)
        except ValueError as e:
            print(f"Error configuring Gemini API: {e}")
            print("Please ensure you have a .env file in your backend directory with GEMINI_API_KEY=YOUR_API_KEY_HERE")
            # Exit or handle the error appropriately if the API key is critical for the application to run.
            # For this example, we'll allow it to continue but the generate_explanation function will fail.


    def generate_explanation(self, prompt: str) -> str:
        """
        Generates an explanation using the Google Gemini 2.5 Flash model.

        Args:
            prompt (str): The input text or code snippet for which an explanation is requested.

        Returns:
            str: The AI-generated explanation, or an error message if something goes wrong.
        """
        if not self.API_KEY:
            return "Error: Gemini API key is not configured. Please check your .env file."

        try:
            # Load grammar description
            grammar_path = os.path.join(os.path.dirname(__file__), "grammar_description.json")
            with open(grammar_path, "r") as f:
                grammar_json = json.load(f)
            readable_grammar = json.dumps(grammar_json, indent=2)

            # Combine grammar and user prompt
            prompt_lines = []

            prompt_lines.append("Analyze the user's code using the grammar.")
            prompt_lines.append("Respond only with technical analysis. No introductions, summaries, or unnecessary details.\n")

            prompt_lines.append("For each line of code, perform the following:")
            prompt_lines.append("1. Lexical: List tokens.")
            prompt_lines.append("2. Parsing: State which grammar rule(s) matched.")
            prompt_lines.append("3. Semantics: Note any semantic meaning or issues.\n")
            prompt_lines.append('If any errors are found, add a final section labeled "Possible Errors" with a brief explanation.Just Syntax Error or Semantic Error.\n')
            prompt_lines.append("Be clear and concise—under 200 words. Use fewer if the code is simple.\n")
        

            prompt_lines.append("Grammar:")
            prompt_lines.append("```json")
            prompt_lines.append(readable_grammar)
            prompt_lines.append("```\n")

            prompt_lines.append("User Prompt:")
            prompt_lines.append("```plaintext")
            prompt_lines.append(prompt)
            prompt_lines.append("```\n")

           

            full_prompt = "\n".join(prompt_lines)
  

            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents= full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction="""You are to provide additional information to the user on the transformations which is the 
                    lexer to the parser then the semantics analyzer taking place from the user code. 
                
                
                    Your job is to:
                    -Be clear but concise max words(200 words no more when generating response)
                    - Explain what the code does clearly and simply
                    - Highlight any possible errors or ambiguities
                    - Give helpful suggestions if needed
                    - Focus on explaining what the code does, not how it's written
                    -Act as if you are thinking out loud as you explain the code

                    Always format your output as follows:
                        1. Use bullet points or numbered lists to organize your explanation
                        2. Use proper new lines and spacing so that everything isn't jumbled up
                        """,
                    temperature=0.5,
                    # thinking_config=types.ThinkingConfig(thinking_budget=-0)
                ),
            )
            print(f"AI Explanation Response: {response.text.strip()}")  # Debugging line to check response

            return  "\n" + response.text.strip() + "\n" 
        except Exception as e:
            return f"An error occurred while generating explanation: {e}"


