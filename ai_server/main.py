from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# 1️⃣ Enable CORS (optional for cross-origin access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:8501"] if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2️⃣ Auth token
API_TOKEN = os.environ.get("GC_API_KEY", "secret123")

# 3️⃣ Swagger-friendly bearer token setup
bearer_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# 4️⃣ Request body schema
class PromptRequest(BaseModel):
    question: str
    context: str = ""
    model: str = "llama3"

# 5️⃣ API route
@app.post("/api/generate")
async def generate(data: PromptRequest, token: HTTPAuthorizationCredentials = Depends(verify_token)):
    payload = {
        "model": data.model,
        "prompt": f"<|system|>You are a GC troubleshooting assistant.\n<|user|>{data.context}\n\nQ: {data.question}",
        "stream": False
    }

    try:
        res = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
        res.raise_for_status()
        return {"response": res.json().get("response", "⚠️ No response")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
