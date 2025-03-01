import openai
import os
from dotenv import load_dotenv

def configure_openai():
    """
    Loads the OpenAI API key from environment variables and sets it for global use.
    """
    load_dotenv()  # Load environment variables from .env
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if openai.api_key is None:
        raise ValueError("❌ OPENAI_API_KEY not found. Make sure it's set in backend/.env")
    
# Call this function once when the app starts
configure_openai()