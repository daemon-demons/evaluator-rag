
import os
from google import genai

def list_models():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("No API key found")
        return

    client = genai.Client(api_key=api_key)
    try:
        # Paging is possible
        pager = client.models.list()
        print("Available Models:")
        for model in pager:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
