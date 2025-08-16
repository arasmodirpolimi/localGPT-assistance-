from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Fetch environment variables
LLM_URL = os.environ.get("LOCAL_LLM_URL", "http://model-runner.docker.internal/engines/v1/")
if not LLM_URL.endswith("/"):
    LLM_URL += "/"
LLM_CHAT_ENDPOINT = f"{LLM_URL}chat/completions"
LLM_MODEL = os.environ.get("LOCAL_LLM_MODEL", "ai/smollm2:360M-Q4_K_M")


@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")

    if not prompt.strip():
        return {"error": "Prompt cannot be empty."}

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(LLM_CHAT_ENDPOINT, json=payload)
        response.raise_for_status()  # raises HTTPError if status is 4xx or 5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {
            "error": "HTTP error occurred",
            "status_code": response.status_code,
            "details": response.text
        }
    except requests.exceptions.RequestException as req_err:
        return {
            "error": "Request failed",
            "details": str(req_err)
        }
    except ValueError:
        return {
            "error": "Invalid JSON response",
            "raw_response": response.text
        }
