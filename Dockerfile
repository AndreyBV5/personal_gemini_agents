FROM python:3.11-slim

WORKDIR /app

# opcional: acelerar pip dentro del contenedor
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Render/Railway definen PORT, usa ese valor en tiempo de ejecución
# Si no existe, por defecto 8080 (útil para local)
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
