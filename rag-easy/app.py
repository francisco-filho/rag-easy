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

@app.post("/embeddings")
async def embeddings(req: EmbeddingRequest):
    embeddings = embedder.embed(req.text)
    persist_embedding(dict(
        body=req.text, category=req.category, metadata=req.metadata, embedding=embeddings))
    return {"embeddings": embeddings, "length": len(embeddings)}

@app.post("/search")
def search(query: SearchRequest):
    resp = vector_query(embedder.embed(query.query), limit=3)
    return resp