from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI
from embedder import OllamaEmbedder
from db import persist_embedding, vector_query

app = FastAPI()
embedder = OllamaEmbedder()

class EmbeddingRequest(BaseModel):
    category: str
    metadata: Union[dict, None]
    text: str

class SearchRequest(BaseModel):
    query: str
    limit: int = 3

@app.post("/embeddings")
async def embeddings(req: EmbeddingRequest):
    embeddings = embedder.embed(req.text)
    persist_embedding(dict(
        body=req.text, category=req.category, metadata=req.metadata, embedding=embeddings))
    return {"embeddings": embeddings, "length": len(embeddings)}

@app.post("/search")
def search(sr: SearchRequest):
    resp = vector_query(embedder.embed(sr.query), limit=3)
    return resp

@app.post("/answer")
def answer(req: SearchRequest):
    texts = vector_query(embedder.embed(req.text), limit=req.limit)
    # mount a request with the top `limit` results`
    # ask to a LLM
    # respond to the user
    return {"response": texts}