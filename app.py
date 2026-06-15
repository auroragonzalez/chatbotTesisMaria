"""
FestAI — Production App
========================
Uso:
  Lanzar el chatbot:
    python app.py

  Descargar el modelo LLM (solo la primera vez):
    python app.py --download-model

  Reconstruir el corpus (antes de lanzar por primera vez o tras actualizar los TXT):
    python app.py --ingest                     # todos los festivales en festival_txts/
    python app.py --ingest --festival warm_up  # solo uno

Variables de entorno (todas tienen valor por defecto):
  CUDA_VISIBLE_DEVICES  GPU a usar            (default: "0")
  VLLM_URL              Endpoint vLLM         (default: http://localhost:8000/v1/completions)
  MODEL_NAME            Modelo en vLLM        (default: microsoft/Phi-3-mini-4k-instruct)
  EMBEDDING_MODEL       Modelo de embeddings  (default: intfloat/multilingual-e5-base)
  EMBEDDING_DEVICE      CPU o CUDA            (default: cuda)
  CHROMA_DIR            Ruta base del VectorDB(default: ./chroma_db)
  DATA_DIR              Carpeta de corpus     (default: ./festival_txts)
  CHUNK_SIZE            Tamaño de chunk       (default: 500)
  CHUNK_OVERLAP         Solapamiento de chunk (default: 50)
  RETRIEVER_K           Docs a recuperar      (default: 4)
  MAX_TOKENS            Tokens de respuesta   (default: 512)
  TEMPERATURE           Temperatura del LLM   (default: 0.3)
  HF_TOKEN              Token de HuggingFace   (default: se pide por teclado si es necesario)
  SERVER_PORT           Puerto de Gradio      (default: 7860)
"""

import os
import sys
import json
import time
import getpass
import argparse
import requests
import gradio as gr
from pathlib import Path
from huggingface_hub import snapshot_download
from huggingface_hub.errors import LocalEntryNotFoundError
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Carga el archivo .env si está presente (las variables de entorno ya definidas
# tienen prioridad, por lo que no interfiere con Docker u otros despliegues).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ─────────────────────────────────────────────
# CONFIG  (todas las variables son anulables con env vars)
# ─────────────────────────────────────────────

os.environ["CUDA_VISIBLE_DEVICES"] = os.getenv("CUDA_VISIBLE_DEVICES", "0")

LLM_URL          = os.getenv("LLM_URL",          os.getenv("VLLM_URL",         "http://localhost:11434/v1/chat/completions"))
MODEL_NAME       = os.getenv("MODEL_NAME",        os.getenv("MODEL_NAME",        "phi3:mini"))
EMBEDDING_MODEL  = os.getenv("EMBEDDING_MODEL",   "intfloat/multilingual-e5-base")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE",  "cuda")
CHROMA_DIR       = Path(os.getenv("CHROMA_DIR",   "./chroma_db"))
DATA_DIR         = Path(os.getenv("DATA_DIR",     "./festival_txts_big"))
CHUNK_SIZE       = int(os.getenv("CHUNK_SIZE",    "500"))
CHUNK_OVERLAP    = int(os.getenv("CHUNK_OVERLAP", "50"))
RETRIEVER_K      = int(os.getenv("RETRIEVER_K",   "4"))
MAX_TOKENS       = int(os.getenv("MAX_TOKENS",    "512"))
TEMPERATURE      = float(os.getenv("TEMPERATURE", "0.3"))
SERVER_PORT      = int(os.getenv("SERVER_PORT",   "7860"))
HF_TOKEN         = os.getenv("HF_TOKEN",          None)
LLM_API_KEY      = os.getenv("LLM_API_KEY",       os.getenv("OLLAMA_API_KEY", None))

# ─────────────────────────────────────────────
# MODEL DOWNLOAD
# ─────────────────────────────────────────────

def _get_token() -> str | None:
    """Devuelve el token HF: env var > input seguro por teclado."""
    token = HF_TOKEN
    if not token:
        print("No se encontró HF_TOKEN en el entorno.")
        token = getpass.getpass("Introduce tu token de HuggingFace (Enter para omitir): ").strip() or None
    return token


def ensure_model_downloaded(model_name: str) -> None:
    """
    Comprueba si el modelo ya está en ~/.cache/huggingface/.
    Si no está, lo descarga usando el token HF disponible.
    """
    print(f"[model] Verificando caché para '{model_name}' ...")
    try:
        snapshot_download(model_name, local_files_only=True)
        print(f"[model] Modelo ya en caché. No es necesario descargar.")
        return
    except (LocalEntryNotFoundError, Exception):
        pass

    print(f"[model] Modelo no encontrado en caché. Iniciando descarga (~8 GB) ...")
    token = _get_token()
    snapshot_download(model_name, token=token)
    print(f"[model] Descarga completada. El modelo está en ~/.cache/huggingface/ ✓")


# Lista de festivales detectada automáticamente desde festival_txts/
def get_festivals():
    """Devuelve la lista de festivales disponibles en tiempo de ejecución."""
    if DATA_DIR.exists() and DATA_DIR.is_dir():
        festivals = sorted(d.name for d in DATA_DIR.iterdir() if d.is_dir())
        return festivals if festivals else ["warm_up"]
    return ["warm_up"]


# ─────────────────────────────────────────────
# PROMPTS POR FASE (pre / durante / post)
# ─────────────────────────────────────────────

PHASE_PROMPTS = {
    "Pre-festival": (
        "El usuario está PLANIFICANDO su visita al festival. "
        "Prioriza información sobre alojamiento, transporte de llegada, "
        "cartel de artistas, gastronomía y actividades en la ciudad."
    ),
    "Durante": (
        "El usuario está EN el festival AHORA MISMO. "
        "Da respuestas breves y operativas: accesos, horarios, normativa, "
        "transporte de vuelta, servicios y emergencias."
    ),
    "Post-festival": (
        "El festival ha terminado. Ayuda al usuario a PROLONGAR su experiencia "
        "en el destino: qué ver, dónde comer, planes turísticos, "
        "merchandising oficial y cómo seguir conectado con el festival."
    ),
}

SYSTEM_BASE = (
    "Eres FestAI, un asistente experto en festivales de música y turismo. "
    "Responde en el MISMO idioma en el que el usuario formule la pregunta (español o inglés) "
    "y SOLO con la información del contexto proporcionado. "
    "Si no tienes información suficiente, indícalo claramente en ese mismo idioma sin inventar datos."
)


# ─────────────────────────────────────────────
# EMBEDDINGS (singleton; se carga una sola vez)
# ─────────────────────────────────────────────

print("[startup] Loading embedding model...", flush=True)
embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={"device": EMBEDDING_DEVICE},
)
print("[startup] Embedding model loaded ✓", flush=True)


# ─────────────────────────────────────────────
# CORPUS INGESTION
# ─────────────────────────────────────────────

def ingest_corpus(festival: str) -> None:
    """
    Lee todos los .txt de festival_txts/<festival>/, los divide en chunks
    y los guarda en una colección Chroma con nombre igual al festival.
    Borra la colección anterior para permitir re-ingestión limpia.
    """
    source_dir = DATA_DIR / festival
    if not source_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta de corpus: {source_dir.resolve()}")

    print(f"[ingest:{festival}] Cargando documentos desde {source_dir} ...")
    loader = DirectoryLoader(
        str(source_dir),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True},
        show_progress=True,
    )
    docs = loader.load()
    print(f"[ingest:{festival}] Documentos cargados: {len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    print(f"[ingest:{festival}] Chunks generados: {len(chunks)}")

    # Elimina la colección existente para garantizar consistencia tras actualizar el corpus
    existing = Chroma(
        collection_name=festival,
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model,
    )
    existing.delete_collection()

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=festival,
        persist_directory=str(CHROMA_DIR),
    )
    print(f"[ingest:{festival}] Corpus guardado en {CHROMA_DIR.resolve()} ✓")


# ─────────────────────────────────────────────
# RETRIEVAL
# ─────────────────────────────────────────────

def get_context(query: str, festival: str) -> str:
    """Recupera los chunks más relevantes del corpus del festival indicado."""
    db = Chroma(
        collection_name=festival,
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model,
    )
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVER_K},
    )
    docs = retriever.invoke(query)
    return "\n\n".join(d.page_content for d in docs)


# ─────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────

def build_prompt(context: str, question: str, phase: str) -> str:
    phase_instruction = PHASE_PROMPTS.get(phase, "")
    return (
        f"{SYSTEM_BASE}\n\n"
        f"Contexto de uso: {phase_instruction}\n\n"
        f"CONTEXTO DEL CORPUS:\n{context}\n\n"
        f"PREGUNTA: {question}\n\n"
        f"RESPUESTA:"
    )


# ─────────────────────────────────────────────
# vLLM CLIENT — streaming SSE
# ─────────────────────────────────────────────

def generate_stream(prompt: str):
    """
    Llama al endpoint LLM (Ollama/OpenAI-compatible) con streaming SSE.
    Soporta tanto /v1/completions (vLLM) como /v1/chat/completions (Ollama).
    """
    url = LLM_URL
    is_chat_api = "/chat/completions" in url

    if is_chat_api:
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "stream": True,
        }
    else:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "stream": True,
        }

    headers = {}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    try:
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=120)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        yield f"[Error de conexión con el modelo: {e}]"
        return

    for raw_line in response.iter_lines():
        if not raw_line:
            continue
        decoded = raw_line.decode("utf-8")
        if not decoded.startswith("data:"):
            continue
        data_str = decoded[len("data:"):].strip()
        if data_str == "[DONE]":
            break
        try:
            data = json.loads(data_str)
            if is_chat_api:
                delta = data["choices"][0].get("delta", {})
                text = delta.get("content", "")
            else:
                text = data["choices"][0].get("text", "")
            if text:
                yield text
        except (json.JSONDecodeError, KeyError, IndexError):
            continue


# ─────────────────────────────────────────────
# CHAT HANDLER (Gradio)
# ─────────────────────────────────────────────

def chat(message: str, history: list, festival: str, phase: str):
    """Genera una respuesta RAG con streaming para Gradio."""
    if not message.strip():
        yield ""
        return

    t0 = time.time()
    context  = get_context(message, festival)
    prompt   = build_prompt(context, message, phase)

    partial = ""
    for chunk in generate_stream(prompt):
        partial += chunk
        yield partial

    print(f"[chat] festival={festival} phase={phase} time={time.time() - t0:.2f}s")


# ─────────────────────────────────────────────
# GRADIO UI
# ─────────────────────────────────────────────

with gr.Blocks(title="FestAI") as demo:
    gr.Markdown(
        "# 🎵 FestAI\n"
        "Asistente inteligente para festivales de música · powered by RAG + open-source LLM"
    )

    # Cargar festivales en tiempo de ejecución
    festivals_available = get_festivals()

    with gr.Row():
        festival_selector = gr.Dropdown(
            choices=festivals_available,
            value=festivals_available[0] if festivals_available else "warm_up",
            label="Festival",
            scale=1,
            interactive=True,
        )
        phase_selector = gr.Radio(
            choices=list(PHASE_PROMPTS.keys()),
            value="Pre-festival",
            label="Momento de uso",
            scale=2,
        )

    gr.ChatInterface(
        fn=chat,
        additional_inputs=[festival_selector, phase_selector],
        chatbot=gr.Chatbot(height=460, label="FestAI"),
        textbox=gr.Textbox(placeholder="Escribe tu pregunta sobre el festival...", label=""),
    )


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FestAI — asistente RAG para festivales")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Reconstruir el corpus en Chroma partiendo de festival_txts/ y salir.",
    )
    parser.add_argument(
        "--festival",
        type=str,
        default=None,
        help="Festival concreto a ingestar. Si se omite, se procesan todos.",
    )
    parser.add_argument(
        "--download-model",
        action="store_true",
        help="Comprobar si el modelo LLM está en caché y descargarlo si no lo está.",
    )
    args = parser.parse_args()

    if args.download_model:
        ensure_model_downloaded(MODEL_NAME)
        sys.exit(0)

    if args.ingest:
        targets = [args.festival] if args.festival else get_festivals()
        if not targets:
            print("No se encontraron carpetas de festival en", DATA_DIR)
            sys.exit(1)
        for fest in targets:
            ingest_corpus(fest)
        print("\nIngestión completada. Lanza el chatbot con: python app.py")
        sys.exit(0)

    print("[startup] Building Gradio UI...")
    demo.launch(server_name="0.0.0.0", server_port=SERVER_PORT)
