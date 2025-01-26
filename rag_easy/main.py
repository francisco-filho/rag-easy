import db
from tqdm.rich import tqdm

emb_example = {
    "category": "example_category",
    "metadata": {"key1": "value1", "key2": "value2"},
    "body": {"name": "jonh", "age": 30},
    "embedding": [0.1323432] * 1024
}

def embed(embedding_data):
    db.persist_embedding(embedding_data)


if __name__ == "__main__":
    from indexer import PdfLoader, PageChunker
    from embedder import OllamaEmbedder

    file = '/home/ff/Downloads/books/aigen.pdf'
    loader = PdfLoader()
    doc = loader.load(file, first_page=0, last_page=-1)

    page_chunker = PageChunker()
    chunks = page_chunker.chunk(doc.pages, metadata=doc.metadata)
    embedder = OllamaEmbedder()

    for c in tqdm(chunks, desc="Embedding"):
        embedding = embedder.embed(c.text)
        data = {
            "category": "book",
            "metadata": doc.metadata,
            "body": c.text,
            "embedding": embedding
        }
        embed(data)