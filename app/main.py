from fastapi import FastAPI
from pydantic import BaseModel
from .gemini_client import generate_json
from .prompts import (
    SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT,
    CLASSIFIER_SYSTEM, CLASSIFIER_PROMPT
)

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

# ===== Endpoints =====
@app.post("/summarize", response_model=SummarizeOut)
def summarize(payload: SummarizeIn):
    data = generate_json(SUMMARIZER_SYSTEM, SUMMARIZER_PROMPT(payload.text))
    return data

@app.post("/classify", response_model=ClassifyOut)
def classify(payload: ClassifyIn):
    data = generate_json(CLASSIFIER_SYSTEM, CLASSIFIER_PROMPT(payload.task))
    return data
