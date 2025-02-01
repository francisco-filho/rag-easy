import os
import ollama
from ollama import EmbedResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from rag_easy.llm import LLMOpenAI

load_dotenv()

HOST = os.getenv('OLLAMA_BASE_URL')
DEFAULT_MODEL = os.getenv("DEFAULT_EMBED_MODEL")

class EmbedProvider(BaseModel):
    def embed(self, input_text: str, model=DEFAULT_MODEL, **kwargs) -> list:
        """ Abstract method """
        pass

class OllamaEmbedder(EmbedProvider):
    def embed(self, input_text: str, model=DEFAULT_MODEL, **kwargs) -> list:
        # sadly, i could not find a way to change the length of the embedding from ollama.
        #response = ollama.embed(model=model, input=input_text, options=kwargs)
        #return response.embeddings[0]
        openai = LLMOpenAI(base_url=HOST, model=model, api_key='ollama')
        embeddings = openai.embed(input_text)
        return embeddings.data[0].embedding

if __name__ == "__main__":
    text = "Hello, world!"
    embedder = OllamaEmbedder()
    vector = embedder.embed(text)
    print(len(vector))