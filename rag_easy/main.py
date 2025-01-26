import db

def embed():
    embedding_data = {
        "category": "example_category",
        "metadata": {"key1": "value1", "key2": "value2"},
        "body": {"name": "jonh", "age": 30},
        "embedding": [0.1323432] * 1024
    }
    db.persist_embedding(embedding_data)
    rows = db.vector_query(embedding_data["embedding"])
    print(rows)


if __name__ == "__main__":
    from indexer import PdfLoader, PageChunker
    file = '/home/ff/Downloads/books/aigen.pdf'
    loader = PdfLoader()
    doc = loader.load(file, first_page=24, last_page=35)

    page_chunker = PageChunker()
    chunks = page_chunker.chunk(doc.pages, metadata=doc.metadata)
    for c in chunks:
        print(c)