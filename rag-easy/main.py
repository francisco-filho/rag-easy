import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

dbname=os.getenv('DB_NAME')
collection="public.myfirstcol"

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host='localhost'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Failed to connect to database: {e}")
        return None

def persist_embedding(data: dict):
    conn = connect_to_db()
    if not conn:
        raise Exception("Could not connect to the database")

    cur = conn.cursor()

    try:
        query = f"""
            INSERT INTO {collection} (category, metadata, body, embedding) 
            VALUES (%s, %s, %s, %s);
            """
        cur.execute(query, (data['category'], json.dumps(data['metadata']), json.dumps(data['body']), data['embedding']))

        conn.commit()

    except psycopg2.Error as e:
        print(f"Failed to persist data: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def vector_query(embedding: list, category=None, limit=5):
    conn = connect_to_db()
    if not conn:
        raise Exception("Could not connect to the database")
    cur = conn.cursor()
    try:
        if category:
            query = f"""
                SELECT id, category, body, metadata FROM {collection} 
                WHERE category = %s
                ORDER BY embedding <-> %s LIMIT %s
                """
            cur.execute(query, (category, str(embedding), limit))
        else:
            query = f"""
                SELECT id, category, body, metadata FROM {collection} 
                ORDER BY embedding <-> %s LIMIT %s
                """
            cur.execute(query, (str(embedding), limit))

        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Failed to query table: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    embedding_data = {
        "category": "example_category",
        "metadata": {"key1": "value1", "key2": "value2"},
        "body": {"name": "jonh", "age": 30},
        "embedding": [0.1323432] * 8192
    }
    persist_embedding(embedding_data)
    rows = vector_query(embedding_data["embedding"])
    print(rows)