"""
constants.py — Configuración NO secreta de FestAI.

Única fuente de verdad para todo lo que no sea un secreto. Estos valores
están versionados a propósito: así el comportamiento del despliegue es
determinista y no depende de variables de entorno que se puedan olvidar
o pisar (p. ej. el lío de DATA_DIR apuntando al corpus equivocado).

Los SECRETOS (claves de API / tokens) NO van aquí: viven en `.env`
  - LLM_API_KEY
  - HF_TOKEN

Las rutas son relativas al directorio de trabajo (WORKDIR=/app en el
contenedor, raíz del proyecto en local), por lo que son válidas en ambos.
"""

# ── GPU ───────────────────────────────────────────────────────────────
CUDA_VISIBLE_DEVICES = "0"

# ── LLM endpoint (Ollama Cloud, formato OpenAI-compatible) ─────────────
LLM_URL    = "https://ollama.com/v1/chat/completions"
MODEL_NAME = "gemma3:27b"

# ── Embeddings (HuggingFace; se descarga en el primer arranque) ────────
EMBEDDING_MODEL  = "intfloat/multilingual-e5-base"
EMBEDDING_DEVICE = "cpu"

# ── Rutas (relativas a WORKDIR; válidas en local y en el contenedor) ───
CHROMA_DIR = "./chroma_db"
DATA_DIR   = "./festival_txts_big"

# ── Caso de uso actual: un único festival ─────────────────────────────
# Festival que se asume cuando el usuario no menciona ninguno.
DEFAULT_FESTIVAL      = "warm_up"                      # carpeta / colección Chroma
FESTIVAL_DISPLAY_NAME = "WARM UP Estrella de Levante"  # nombre legible para el prompt

# ── RAG ────────────────────────────────────────────────────────────────
CHUNK_SIZE    = 1200
CHUNK_OVERLAP = 150
RETRIEVER_K   = 10
MAX_TOKENS    = 1500
TEMPERATURE   = 0.3

# ── Servidor Gradio ────────────────────────────────────────────────────
SERVER_PORT = 8000
