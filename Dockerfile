FROM python:3.11-slim

WORKDIR /app

# Install CPU-only torch first (much smaller than CUDA version)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu sentence-transformers

# Install remaining dependencies (skip torch and sentence-transformers, already installed)
COPY requirements.txt .
RUN pip install --no-cache-dir $(sed '/^torch/d; /^sentence-transformers/d; /^#/d; /^\s*$/d' requirements.txt | tr '\n' ' ')

# Copy app files
COPY app.py .
COPY chroma_db/ ./chroma_db/
COPY festival_txts/ ./festival_txts/
COPY contexto/ ./contexto/

# CPU-only config
ENV PYTHONUNBUFFERED=1
ENV EMBEDDING_DEVICE=cpu
ENV VLLM_URL=http://ollama:11434/v1/completions
ENV MODEL_NAME=phi3:mini
ENV SERVER_PORT=7860

EXPOSE 7860

CMD ["python", "app.py"]