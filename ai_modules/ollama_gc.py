# ollama_gc.py
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # change to your local Ollama model if needed

def ask_ollama(question):
    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return response.json().get('response', '')
    else:
        return f"Error: {response.status_code} {response.text}"
