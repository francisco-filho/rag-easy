import db

if __name__ == "__main__":
    embedding_data = {
        "category": "example_category",
        "metadata": {"key1": "value1", "key2": "value2"},
        "body": {"name": "jonh", "age": 30},
        "embedding": [0.1323432] * 1024
    }
    db.persist_embedding(embedding_data)
    rows = db.vector_query(embedding_data["embedding"])
    print(rows)