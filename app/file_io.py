# app/file_io.py
from typing import Tuple
from pypdf import PdfReader
from docx import Document as DocxDocument

def read_pdf_bytes(b: bytes) -> str:
    from io import BytesIO
    reader = PdfReader(BytesIO(b))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)

def read_docx_bytes(b: bytes) -> str:
    from io import BytesIO
    doc = DocxDocument(BytesIO(b))
    return "\n".join(p.text for p in doc.paragraphs)

def read_txt_bytes(b: bytes, encoding: str = "utf-8") -> str:
    try:
        return b.decode(encoding, errors="ignore")
    except Exception:
        return b.decode("latin-1", errors="ignore")

def extract_text_from_upload(filename: str, content_type: str, raw: bytes) -> Tuple[str, str]:
    """
    Devuelve (texto, tipo_detectado) según extensión/content_type.
    """
    name = (filename or "").lower()
    ctype = (content_type or "").lower()

    if name.endswith(".pdf") or "pdf" in ctype:
        return read_pdf_bytes(raw), "pdf"
    if name.endswith(".docx") or "word" in ctype or "officedocument" in ctype:
        return read_docx_bytes(raw), "docx"
    # fallback txt/markdown
    return read_txt_bytes(raw), "txt"
