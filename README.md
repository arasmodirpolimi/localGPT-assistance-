
## 📌 Project Name: LocalGPT Assistant – `Docker Model Runner Edition`

### 👥 Team Context

This project is part of an exploration into local-first AI development. The idea is to empower developers to build ChatGPT-style apps without depending on cloud APIs, by leveraging Docker Model Runner as a local inference backend.

The goal is to demonstrate how you can integrate local models into an existing FastAPI + Gradio stack and orchestrate everything with Docker Compose.

---

## 🎯 Mission Objective

> **Integrate Docker Model Runner as the local LLM backend for an existing ChatGPT-style app, replacing external API calls.**

This will allow:

* ⚡ Local inference with open-source LLMs (SmolLM, TinyLlama, Gemma, etc.)

* 📦 Reproducible deployments via Docker Compose

* 🔒 Offline or air-gapped development environments

---

## 🧱 Provided Project Structure

You are given the following repository:

```
localgpt/
├── LICENSE
├── README.md
├── app/
│   ├── main.py              # FastAPI backend for prompt handling
│   ├── Dockerfile
│   └── requirements.txt
├── ui/
│   ├── app.py               # Gradio frontend
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yaml      # [To be created by YOU]
```

---

## 🧩 Project Steps

### 🔍 Phase 1: Learn and Explore Docker Model Runner

Before integrating, understand how Docker Model Runner works:

1. ✅ Enable it in Docker Desktop:

   * Settings > Features in Development > Enable Docker Model Runner

   * Restart Docker Desktop

2. ✅ Try out basic commands:

⠀
```
docker model pull ai/smollm2
docker model run ai/smollm2 "How do you work?"
```

👉 Observe how it pulls, loads, and responds with no external API involved.

---

### 🛠️ Phase 2: Modify FastAPI to Use Local Model

Update `app/main.py` to interact with the Model Runner's OpenAI-compatible endpoint:

```
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
```

✅ This allows FastAPI to relay prompts to the local LLM using a standard OpenAI-style API.

---

### ⚙️ Phase 3: Write Docker Compose Spec

Create a `docker-compose.yaml` that:

* Starts the Docker Model Runner model provider

* Boots the FastAPI and UI containers in correct sequence

* Automatically injects model metadata to services

```
version: "3"

services:
  model:
    provider:
      type: model
      options:
        model: ai/smollm2

  fastapi:
    build:
      context: ./app
    ports:
      - "8000:8000"
    depends_on:
      - model

  ui:
    build:
      context: ./ui
    ports:
      - "8501:8501"
    depends_on:
      - fastapi
```

📌 **Note**: No changes are needed in the UI — it communicates with the FastAPI backend as before.

---

## 🧪 How to Run the Stack

```
docker compose up --build
```

Visit:

* [http://localhost:8501](http://localhost:8501/) – UI

* [http://localhost:8000/chat](http://localhost:8000/chat) – API

---

## 🧠 Learning Goals

By the end of this project, you’ll:

✅ Understand **how Docker Model Runner manages and runs LLMs locally**  
✅ Replace hosted LLM APIs with **local inference endpoints**  
✅ Learn how to **package model providers in Docker Compose**  
✅ Build confidence in **open-source model deployment workflows**  

