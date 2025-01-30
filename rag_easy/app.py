import logging
from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from rag_easy.embedder import OllamaEmbedder
from rag_easy.db import persist_embedding, vector_query
from rag_easy.llm import LLMOllamaWithHistory

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

load_dotenv()

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
    texts = vector_query(embedder.embed(req.query), limit=req.limit)
    info = "\n\n".join([t.body for t in texts])
    logger.info(f"Context retrieved:\n{info}")

    prompt = f"""
    Answer the following question:
    {req.query}

    Evaluate if The following information can help you respond:
    <context>
    {info}
    </context>
    """
    llm = LLMOllamaWithHistory(model="deepseek-r1:14b")

    logger.info(f"Prompt: {prompt}")
    response = llm.chat(prompt)
    logger.info(response)

    return {"response": response}