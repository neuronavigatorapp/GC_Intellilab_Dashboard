import requests

def ollama_predict(prompt, model="llama3"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    response.raise_for_status()

    result = response.json()
    return result["response"]

# Simple test function to verify locally
if __name__ == "__main__":
    test_prompt = "Give a brief summary of Gas Chromatography."
    prediction = ollama_predict(test_prompt)
    print(prediction)
