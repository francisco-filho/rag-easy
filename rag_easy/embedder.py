import os
import ollama
from ollama import EmbedResponse
from pydantic import BaseModel


DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")

class EmbedProvider(BaseModel):
    def embed(self, input_text: str, model=DEFAULT_MODEL, **kwargs) -> list:
        """ Abstract method """
        pass

class OllamaEmbedder(EmbedProvider):
    def __init__(self):
        super().__init__()

    def embed(self, input_text: str, model=DEFAULT_MODEL, **kwargs) -> list:
        # sadly, i could not find a way to change the length of the embedding from ollama.
        response = ollama.embed(model=model, input=input_text, options=kwargs)
        return response.embeddings[0]

if __name__ == "__main__":
    text = "Hello, world!"
    embedder = OllamaEmbedder()
    vector = embedder.embed(text)
    print(len(vector))