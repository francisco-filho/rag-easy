import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from rag_easy.embedder import OllamaEmbedder
from rag_easy.retriever import SearchRequest, EmbeddingRequest
from rag_easy.db import persist_embedding, vector_query
from rag_easy.llm import LLMOpenAI
from rag_easy.retriever.retriever import VectorRetriever

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

load_dotenv()

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
BASE_URL = os.getenv("OLLAMA_BASE_URL")

app = FastAPI()
embedder = OllamaEmbedder()


@app.post("/embeddings")
async def embeddings(req: EmbeddingRequest):
    embeddings = embedder.embed(req.text)
    persist_embedding(dict(
        body=req.text, category=req.category, metadata=req.metadata, embedding=embeddings))
    return {"embeddings": embeddings, "length": len(embeddings)}

@app.post("/search")
def search(sr: SearchRequest):
    resp = vector_query(embedder.embed(sr.query), limit=2)
    return resp

@app.post("/answer")
def answer(req: SearchRequest):
    retriever = VectorRetriever()
    rows = retriever.retrieve_similar_records(req)
    info = "\n\n".join([t.body for t in rows])

    logger.info([m.metadata for m in rows])

    prompt = f"""
    Responda a seguinte pergunta:
    <pergunta>
    {req.query}
    </pergunta>

    <Contexto>
    {info}
    </Contexto>
    """
    system_message="Você é um especialista na plataforma de IA e você pensa e responde em português"
    llm = LLMOpenAI(model=DEFAULT_MODEL, system=system_message, base_url=BASE_URL)

    logger.info("-"*50)
    logger.info(f"Prompt: {prompt}")
    logger.info("-"*50)
    response = llm.chat(prompt)
    logger.info(response)

    return {"response": response}