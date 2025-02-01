import logging
from pydantic import BaseModel
from rag_easy.embedder import OllamaEmbedder
from .models import SearchRequest, EmbeddingRequest
from rag_easy.db import vector_query

logger = logging.getLogger(__name__)

class Retriever(BaseModel):
    pass

class VectorRetriever(Retriever):
    embedder: object

    def __init__(self, embedder=None):
        super().__init__(embedder=OllamaEmbedder())

    def retrieve_similar_records(self, req: SearchRequest):
        return vector_query(self.embedder.embed(req.query), limit=req.limit)
