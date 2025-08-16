
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

    chatbot = gr.Chatbot(label="LocalGPT", type="messages")
    msg_input = gr.Textbox(placeholder="Type your message here...", show_label=False)
    clear_btn = gr.Button("🧹 Clear")

    msg_input.submit(fn=query_llm, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
    clear_btn.click(fn=lambda: ([], ""), outputs=[chatbot, msg_input])

demo.launch(server_name="0.0.0.0", server_port=8501)