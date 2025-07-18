import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"  # Ensure Ollama is running locally

DEFAULT_MODEL = "llama3"  # Change to mistral, codellama, etc., as desired

def ask_ollama(user_question, model=DEFAULT_MODEL):
    system_prompt = (
        "You are a virtual GC expert trained on ASTM and GPA methods, column behavior, "
        "detector troubleshooting, and method development. Use clear, technical reasoning. "
        "Only make recommendations grounded in analytical chemistry."
    )

    payload = {
        "model": model,
        "prompt": f"<|system|>{system_prompt}\n<|user|>{user_question}",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "⚠️ No response from Ollama.")
    except requests.exceptions.RequestException as e:
        return f"❌ Ollama request failed: {e}"
