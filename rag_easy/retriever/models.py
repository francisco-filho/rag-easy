from typing import Union
from pydantic import BaseModel

class EmbeddingRequest(BaseModel):
    category: str
    metadata: Union[dict, None]
    text: str

class SearchRequest(BaseModel):
    query: str
    limit: int = 3