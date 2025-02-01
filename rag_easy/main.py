import db
import click
import warnings
from tqdm import tqdm
from tqdm import TqdmExperimentalWarning
from indexer import PdfLoader, PageChunker, DirectoryFileScanner
from embedder import OllamaEmbedder
from rag_easy.indexer.indexer import TextLoader
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings('ignore', category=TqdmExperimentalWarning)

def embed(embedding_data):
    db.persist_embedding(embedding_data)
    
@click.group()
def indexer():
    pass

def abort_command(ctx, param, value):
    if not value:
        ctx.abort()

@indexer.command()
@click.option('--collection', required=True, help='Name of the collection to remove from index.')
@click.option('--yes', is_flag=True, 
              expose_value=False, 
              prompt="Delete the entire collection?",
              callback=abort_command)
def clear(collection: str):
    db.clear_index(collection)
    print(f"Collection {collection} is now EMPTY")


@indexer.command()
@click.option('--directory', required=True, help='Path to the directory containing PDF files.')
@click.option('--category', required=True, help='Category of the content')
def index_directory(directory: str, category: str):
    file_scanner = DirectoryFileScanner()
    #for file in tqdm(file_scanner.scan(directory)):
    for file in tqdm(file_scanner.listFiles(directory)):
        loader = TextLoader()
        c = loader.load(file)
        embedder = OllamaEmbedder()
        content = c.content
        embedding = embedder.embed(content)
        data = {
            "category": category,
            "metadata": c.metadata,
            "body": content,
            "embedding": embedding
        }
        embed(data)


@indexer.command()
@click.option('--file', required=True, help='Path to the PDF file.')
@click.option('--category', required=True, help='Category of the content')
def index_file(file: str, category: str):
    loader = PdfLoader()
    doc = loader.load(file, first_page=0, last_page=-1)
    page_chunker = PageChunker()
    chunks = page_chunker.chunk(doc.pages, metadata=doc.metadata())
    embedder = OllamaEmbedder()

    for c in tqdm(chunks, desc="Embedding"):
        if not c.text:
            continue
        embedding = embedder.embed(c.text)
        data = {
            "category": category,
            "metadata": c.metadata,
            "body": c.text,
            "embedding": embedding
        }
        embed(data)

# todo: add options for aditional metadata
#@click.command()
#@click.option('--file', required=True, help='Path to the PDF file.')
#@click.option('--category', required=True, help='Category of the content')
def main(file: str, category: str):
    loader = PdfLoader()
    doc = loader.load(file, first_page=0, last_page=-1)
    page_chunker = PageChunker()
    chunks = page_chunker.chunk(doc.pages, metadata=doc.metadata)
    embedder = OllamaEmbedder()

    for c in tqdm(chunks, desc="Embedding"):
        embedding = embedder.embed(c.text)
        data = {
            "category": category,
            "metadata": c.metadata,
            "body": c.text,
            "embedding": embedding
        }
        embed(data)


if __name__ == "__main__":
    indexer()