import gradio as gr
import requests

# Stores OpenAI-style message list
chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

def query_llm(message, history):
    # Append user message to history
    history.append({"role": "user", "content": message})

    try:
        response = requests.post("http://fastapi:8000/chat", json={"prompt": message})
        reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error")
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    history.append({"role": "assistant", "content": reply})
    return "", history

with gr.Blocks(css="footer {display:none !important}") as demo:
    gr.Markdown("## 💬 LocalGPT Chat — Self-Hosted ChatGPT UI\n_Docker Model Runner + FastAPI + Gradio_")