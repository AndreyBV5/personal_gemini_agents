# app/pipeline.py
from typing import List, Dict
from .gemini_client import generate_json
from .prompts import SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT, CLASSIFIER_SYSTEM, CLASSIFIER_PROMPT

def chunk_text(text: str, max_chars: int = 7000, overlap: int = 300) -> List[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+max_chars]
        chunks.append(chunk)
        i += max_chars - overlap
    return chunks

def summarize_long_text(text: str) -> Dict:
    """
    Map-Reduce simple:
      1) resumen por chunk
      2) resumen final a partir de los resúmenes parciales
    """
    chunks = chunk_text(text)
    if len(chunks) == 1:
        return generate_json(SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT(chunks[0]))

    partials = []
    for ch in chunks:
        p = generate_json(SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT(ch))
        partials.append(f"- {p.get('tldr','')}\n" + "\n".join([f"* {b}" for b in p.get('bullets', [])]))

    merged_text = "Resúmenes parciales:\n" + "\n\n".join(partials)
    return generate_json(SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT(merged_text))

def classify_text(text: str) -> Dict:
    # Usar solo el inicio para evitar prompt demasiado largo
    head = text[:4000]
    return generate_json(CLASSIFIER_SYSTEM, CLASSIFIER_PROMPT(head))
