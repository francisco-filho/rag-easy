from typing import Union
from datetime import datetime
from pydantic import BaseModel

class Page(BaseModel):
    index: int
    content: str

    def summary(self) -> str:
        max_size = 100
        content = self.content[:max_size] + "..." if len(self.content) > max_size else self.content
        return f"Page {self.index}:\n{content}"

class Document(BaseModel):
    title: Union[str, None]
    author: str
    date: datetime
    subject: Union[str, None] = None
    pages: list[Page]

    def __str__(self):
        return f"Document(title={self.title}, author={self.author}, date={self.date}, subject={self.subject})"

    @property
    def metadata(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "date": self.date.strftime("%Y-%m-%d"),
            "subject": self.subject
        }

class Chunk(BaseModel):
    index: str
    metadata: dict
    text: str

    def __str__(self):
        return f"Chunk(index={self.index}, metadata={self.metadata}, text={self.text[0:16]}...)"