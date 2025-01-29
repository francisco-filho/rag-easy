from typing import Generator
from tqdm.rich import tqdm
from pypdf import PdfReader
from pydantic import BaseModel
from pathlib import Path
from .models import Page, Document, Chunk

class Chunker(BaseModel):
    pass

# todo: RegexChunker, WordChunker


class PageChunker(Chunker):
    def chunk(self, pages: list[Page], metadata={},overlap: int = 1) -> list[Chunk]:
        result = []
        c = 0
        while c < len(pages):
            text = ""
            for i in range(overlap):
                if c > len(pages)-overlap:
                    text = text + pages[c].content
                else:
                    text = text + pages[c+i].content
            pm = metadata.copy()
            pm["page"] = pages[c].index
            result.append(Chunk(index=str(pages[c].index), text=text, metadata=pm))
            c = c + 1
                
        return result

class Loader(BaseModel):
    def load(self, *args, **kwargs):
        raise NotImplementedError

class DirectoryFileScanner():
    def scan(self, fp: str, extension=['.md', '.txt']) -> Generator[Path, None, None]:
        for f in Path(fp).glob("**/*"):
            if f.is_file() and f.suffix.lower() in extension:
                yield f
        return None

class TextLoader(Loader):
    def load(self, fp: str) -> Document:
        with open(fp, 'r', encoding='utf-8') as f:
            return Document(
                title=f.name,
                author="Unknown",
                pages=[Page(index=0, content=f.read())],
                date=None,
                metadata={
                    "root_dir": fp.parent,
                    "filename": f.name,
                    "extension": "",
                    "path": str(fp),
                })

class PdfLoader(Loader):
    def load(self, fp: str, first_page=0, last_page=-1, remove_footer=True) -> Document:
        if not Path(fp).exists():
            raise FileNotFoundError(f"File {fp} does not exist")
        return self._read_pdf(fp, first_page, last_page, remove_footer)

    def _read_pdf(self, file, first_page=24, last_page=-1, remove_footer=True) -> Document:
        def visitor_fn(text, cm, tm, font_dict, font_size):
            y = cm[5]
            if 150 < y < 500 and text:
                pages_acc.append(text)

        pages = []                
        pages_acc = []   
        doc = PdfReader(file)
        
        for i, p in enumerate(tqdm(doc.pages[first_page:last_page], desc="Reading document")):
            if remove_footer:
                pages.append(Page(index=p.page_number, content=p.extract_text(visitor_text=visitor_fn).strip()))
            else:
                pages.append(Page(index=p.page_number, content=p.extract_text().strip()))

        return Document(
            title=doc.metadata.title,
            author=doc.metadata.author,
            subject=doc.metadata.subject,
            date=doc.metadata.creation_date,
            pages=pages
        )

