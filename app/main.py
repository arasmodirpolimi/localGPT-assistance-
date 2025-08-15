from fastapi import FastAPI, Request
import requests

app = FastAPI()
LLM_URL = "http://model-runner.docker.internal/engines/llama.cpp/v1/chat/completions"

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt")
    payload = {
        "model": "ai/smollm2",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(LLM_URL, json=payload)
    return response.json()
