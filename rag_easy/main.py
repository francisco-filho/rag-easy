import db
import click
from tqdm.rich import tqdm
from indexer import PdfLoader, PageChunker
from embedder import OllamaEmbedder

emb_example = {
    "category": "example_category",
    "metadata": {"key1": "value1", "key2": "value2"},
    "body": {"name": "jonh", "age": 30},
    "embedding": [0.1323432] * 1024
}

def embed(embedding_data):
    db.persist_embedding(embedding_data)

@click.command()
@click.option('--file', required=True, help='Path to the PDF file.')
def main(file: str):
    loader = PdfLoader()
    doc = loader.load(file, first_page=0, last_page=-1)
    page_chunker = PageChunker()
    chunks = page_chunker.chunk(doc.pages, metadata=doc.metadata)
    embedder = OllamaEmbedder()

    for c in tqdm(chunks, desc="Embedding"):
        embedding = embedder.embed(c.text)
        data = {
            "category": "book",
            "metadata": c.metadata,
            "body": {"text": c.text},
            "embedding": embedding
        }
        embed(data)


if __name__ == "__main__":
    main()

    """
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
        """