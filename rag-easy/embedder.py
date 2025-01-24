import ollama
from ollama import EmbedResponse

default_model = 'bge-m3:latest'

def embed(input_text: str, model=default_model) -> list:
    response = ollama.embed(model=model, input=input_text)
    return response.embeddings[0]