# app/gemini_client.py
import os
import json
from dotenv import load_dotenv
from google import genai

# 1) Cargar variables del .env ANTES de leerlas
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

if not GEMINI_API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY en el entorno (.env).")

# 2) Crear cliente del SDK nuevo (google-genai)
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_json(system_message: str, user_message: str) -> dict:
    """
    Envía un único string (system + user) y fuerza respuesta JSON.
    Esto evita los errores de validación del SDK cuando se envía
    una lista de dicts estilo 'role/parts'.
    """
    prompt = f"{system_message.strip()}\n\n{user_message.strip()}"

    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,  # 👈 un solo string
        config={"response_mime_type": "application/json"},
    )

    # Intentar parsear JSON; si falla, devolver algo informativo
    try:
        return json.loads(resp.text)
    except Exception as e:
        return {
            "error": "La respuesta no fue JSON válido.",
            "raw": resp.text,
            "details": str(e),
        }
