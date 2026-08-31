# LLM Service Module
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)  # Load environment variables from .env file

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # Default to "gemini-2.0-flash" if not set

if not API_KEY:
    raise ValueError(f"GEMINI_API_KEY is not set in .env at: {ENV_FILE}")

print(f"Using .env: {ENV_FILE}")
print(f"Using model: {MODEL_NAME}")
print(f"API key loaded: {'YES' if API_KEY else 'NO'}")

client = genai.Client(api_key=API_KEY)

def generate_response(prompt:str, json_mode: bool=False) -> str:
    """Send a prompt to Gemini and return the generated response."""
    config=None

    if json_mode:
        config = types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text