# Sistema para resúmenes
SUMMARIZER_SYSTEM = """You are a concise summarization assistant.
- Output Spanish.
- Return valid JSON only.
- Provide 3-7 bullet points and one TLDR under 200 chars.
"""

def SUMMARIZER_PROMPT(text: str) -> str:
    return f"""
Texto de entrada:
{text}

Devuelve JSON con esta forma:
{{
  "bullets": ["...","...","..."],
  "tldr": "..."
}}
"""

# Sistema para clasificador de tareas
CLASSIFIER_SYSTEM = """You are a task classifier.
- Output Spanish.
- Return valid JSON only.
- Categories: ["Reuniones","Documentación","Finanzas","Soporte","Ventas","Otro"]
- Priority: ["alta","media","baja"]
"""

def CLASSIFIER_PROMPT(task: str) -> str:
    return f"""
Tarea:
{task}

Devuelve JSON con esta forma:
{{
  "category": "Reuniones|Documentación|Finanzas|Soporte|Ventas|Otro",
  "priority": "alta|media|baja",
  "keywords": ["...","..."],
  "suggested_title": "título breve en español"
}}
"""
