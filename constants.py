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
# CHUNK_SIZE=3200 para que cada unidad coherente viva en UN solo chunk y el
# retriever no devuelva media unidad. El límite lo marca el cartel completo de
# un día (4 escenarios) MÁS sus cabeceras bilingües (ES+EN), ~2570 chars, y la
# ficha de "cómo llegar" con los 4 medios (~2820). Con 2500 estos ficheros se
# partían y se perdían las horas/algún medio; 3200 los mantiene íntegros.
CHUNK_SIZE    = 3200
CHUNK_OVERLAP = 300
# RETRIEVER_K=10: con las fichas consolidadas (cartel diario completo en un
# chunk; "cómo llegar" con los 4 medios en un chunk) y las cabeceras en lenguaje
# natural de los horarios, la ficha autoritativa rankea arriba y k=10 basta.
# Se usa búsqueda por SIMILARITY (no MMR): al estar el contenido consolidado,
# diversificar (MMR) solo introducía chunks distractores.
RETRIEVER_K   = 10
MAX_TOKENS    = 1500
# TEMPERATURE=0.1 (bajada desde 0.3): un asistente factual necesita respuestas
# consistentes; a 0.3 se observaban saltos de idioma puntuales y alguna cifra a
# la deriva. 0.1 prioriza fidelidad y estabilidad sin quedar totalmente rígido.
TEMPERATURE   = 0.1

# ── Ingesta: exclusiones ───────────────────────────────────────────────
# Las noticias de prensa (previsiones meteorológicas puntuales, rumores de
# cartel de ediciones pasadas, etc.) contaminaban respuestas de datos estables
# (clima general, transporte, cartel). Se excluyen del corpus principal; las
# fichas oficiales siguen cubriendo esos temas. Patrones glob relativos a la
# carpeta del festival.
INGEST_EXCLUDE_GLOBS = [
    "**/salida_laverdad_warmup_tema/**",
    "**/noticias_depuradas/**",
    # Resumen agregado de bandas (CSV volcado a texto). Es redundante con las
    # fichas individuales de cada banda y, además, su columna día/escenario
    # contradice el horario oficial (p. ej. anuncia artistas que el cartel
    # final no incluye), contaminando las respuestas de "quién toca el día X".
    "**/00_bandas_warmup_resumen*",
]

# ── Servidor Gradio ────────────────────────────────────────────────────
SERVER_PORT = 8000
