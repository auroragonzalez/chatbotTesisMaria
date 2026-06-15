FROM python:3.11-slim

WORKDIR /app

# Install CPU-only torch first (much smaller than CUDA version)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu sentence-transformers

# Install remaining dependencies (skip torch and sentence-transformers, already installed)
COPY requirements.txt .
RUN pip install --no-cache-dir $(sed '/^torch/d; /^sentence-transformers/d; /^#/d; /^\s*$/d' requirements.txt | tr '\n' ' ')

# ── Aplicación ────────────────────────────────────────────────────────
COPY app.py .
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# ── Corpus de PRODUCCIÓN: festival_txts_big (warm_up enriquecido) ──────
# Es el mismo corpus que el .env local (DATA_DIR=./festival_txts_big).
COPY festival_txts_big/ ./festival_txts_big/

# ── Índice Chroma prehorneado (construido desde festival_txts_big) ────
# Sirve como fallback si no se monta un volumen. El entrypoint lo
# reconstruye si falta o si INGEST_ON_START=1.
COPY chroma_db/ ./chroma_db/

# ── Configuración CPU-only y rutas de datos ───────────────────────────
ENV PYTHONUNBUFFERED=1
ENV EMBEDDING_DEVICE=cpu
ENV SERVER_PORT=7860
ENV CHROMA_DIR=/app/chroma_db
ENV DATA_DIR=/app/festival_txts_big

EXPOSE 7860

ENTRYPOINT ["./docker-entrypoint.sh"]
