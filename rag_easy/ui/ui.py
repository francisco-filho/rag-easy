import re
import json
import gradio as gr
from gradio import ChatMessage
from rag_easy.llm import LLMOpenAI

llm = LLMOpenAI(model="deepseek-r1:8b")

def fix_markdown_linebreak(s):
    return re.sub("\n", "<br/>", s, re.DOTALL)

def chat_response(message, history):
    resp = fix_markdown_linebreak(llm.chat(message, history))
    print(resp)
    history.append(ChatMessage(role="assistant", content=resp).__dict__)
    print("words: ", len(json.dumps(history).split()))
    return "", history


with gr.Blocks() as localchat:
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    msg.submit(chat_response, [msg, chatbot], [msg, chatbot])

localchat.launch()
    