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
COPY constants.py .
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# ── Corpus de PRODUCCIÓN: festival_txts_big (warm_up enriquecido) ──────
# DATA_DIR=./festival_txts_big está fijado en constants.py.
COPY festival_txts_big/ ./festival_txts_big/

# Toda la configuración (rutas, RAG, modelo, dispositivo) vive en
# constants.py. Aquí solo lo estrictamente del runtime de Python.
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

ENTRYPOINT ["./docker-entrypoint.sh"]
