# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from .gemini_client import generate_json
from .prompts import (
    SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT,
    CLASSIFIER_SYSTEM, CLASSIFIER_PROMPT
)
# 👇 nuevos imports para analizar archivos
from .file_io import extract_text_from_upload
from .pipeline import summarize_long_text, classify_text

app = FastAPI(title="Gemini Agents: Summarizer & Task Classifier")

# ===== Schemas =====
class SummarizeIn(BaseModel):
    text: str

class SummarizeOut(BaseModel):
    bullets: list[str]
    tldr: str

class ClassifyIn(BaseModel):
    task: str

class ClassifyOut(BaseModel):
    category: str
    priority: str
    keywords: list[str]
    suggested_title: str

# Para /analyze-file
class FileAnalyzeOut(BaseModel):
    detected_type: str
    summarize: SummarizeOut | None = None
    classify: ClassifyOut | None = None
    chars: int

# ===== Endpoints existentes =====
@app.post("/summarize", response_model=SummarizeOut)
def summarize(payload: SummarizeIn):
    data = generate_json(SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT(payload.text))
    return data

@app.post("/classify", response_model=ClassifyOut)
def classify(payload: ClassifyIn):
    data = generate_json(CLASSIFIER_SYSTEM, CLASSIFIER_PROMPT(payload.task))
    return data

# ===== Nuevo endpoint: subir archivo y analizar =====
@app.post("/analyze-file", response_model=FileAnalyzeOut)
async def analyze_file(
    file: UploadFile = File(...),
    do_summarize: bool = True,
    do_classify: bool = True,
):
    raw = await file.read()

    # Límite básico de tamaño (12 MB)
    if len(raw) > 12 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande (máx ~12MB).")

    text, detected = extract_text_from_upload(file.filename, file.content_type, raw)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del archivo.")

    out_sum = summarize_long_text(text) if do_summarize else None
    out_cls = classify_text(text) if do_classify else None

    return {
        "detected_type": detected,
        "summarize": out_sum,
        "classify": out_cls,
        "chars": len(text),
    }
