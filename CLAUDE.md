# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

FestGPT is a RAG-based chatbot for music festivals (Gradio UI + LangChain + ChromaDB + external LLM). The entire application is a single-file Python app (`app.py`, ~400 lines). It is part of a PhD thesis targeting a 2026 special issue on LLMs for tourism.

## Common commands

```bash
# First-time setup
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Download the embedding model (happens automatically on first import) and optionally the LLM
python app.py --download-model

# Ingest the knowledge corpus (rebuilds ChromaDB from festival_txts/)
python app.py --ingest                      # all festivals
python app.py --ingest --festival warm_up   # single festival

# Launch the chatbot (Gradio on port 7860)
python app.py

# Run evaluation benchmark (see "Known breakage" below — currently fails to import)
python eval/run_eval.py --models phi3 salamandra mistral qwen
```

### Docker (production deployment)

```bash
# Build + run; reads .env, mounts ./chroma_db and ./festival_txts, forces EMBEDDING_DEVICE=cpu
docker compose up --build
```

The container runs the Gradio app on port 7860 with a healthcheck. It does **not** run `--ingest`; populate `chroma_db/` on the host first (the volume is bind-mounted) or exec the ingest command inside the container.

## Architecture

**Single-file app (`app.py`)** — also acts as a library imported by `eval/run_eval.py`. Key sections in order:

1. **Config** (lines 53-68): all settings via `os.getenv` with defaults. Accepts both `LLM_URL` (primary) and `VLLM_URL` (fallback) for the LLM endpoint.
2. **Embeddings singleton** (line 144): `HuggingFaceEmbeddings` with `multilingual-e5-base` loads at **import time**, not lazily. This means any script that imports `app` pays the embedding model load cost immediately.
3. **Corpus ingestion** (`ingest_corpus`): loads `.txt` files via `DirectoryLoader`, splits with `RecursiveCharacterTextSplitter`, stores in Chroma with one **collection per festival** (collection name = folder name). Deletes and rebuilds the collection on each run.
4. **Retrieval** (`get_context`): similarity search returning top-k chunks from the festival's Chroma collection.
5. **Prompt construction** (`build_prompt`): assembles `SYSTEM_BASE` + phase instruction + retrieved context + user question. Three phases: Pre-festival, Durante, Post-festival.
6. **LLM streaming** (`generate_stream`): SSE-based streaming via `requests`. Auto-detects `/v1/chat/completions` (Ollama/OpenAI format) vs `/v1/completions` (vLLM format) based on the URL string. Supports `LLM_API_KEY` for cloud providers.
7. **Gradio UI**: `gr.Blocks` with festival dropdown (auto-populated from `festival_txts/` subdirectories), phase radio, and `gr.ChatInterface`.
8. **CLI**: argparse with `--ingest`, `--festival`, `--download-model`.

**Festival auto-detection**: `get_festivals()` scans `festival_txts/` for subdirectories at runtime. Adding a new festival is just creating a folder with `.txt` files and re-ingesting.

**Corpus format**: plain-text Spanish files organized by festival and topic (`faq.txt`, `horarios.txt`, `accesos.txt`, `transporte.txt`). One idea per paragraph or Q&A format. Ingestion globs `**/*.txt` recursively, so nested topic folders are fine.

**Two corpora**:
- `festival_txts/` — the committed corpus and the default `DATA_DIR`. Three festivals: `animal_sound`, `mar_de_musicas`, `warm_up`, each with the four canonical topic files.
- `festival_txts_big/` — an untracked, richer warm_up corpus (granular topic folders, plus `.csv`/`.jpg` assets and macOS junk like `__MACOSX/`/`.DS_Store`). Its real content lives one level down in `festival_txts_big/festival_txts/`. To use it, point `DATA_DIR` at that inner path and re-ingest; only `**/*.txt` is loaded (CSV/JPG are ignored).

**Evaluation** (`eval/`): `qa_benchmark.json` (17 questions across phases + out-of-scope hallucination checks) + `run_eval.py` (ROUGE-L, BERTScore F1 Spanish, latency, hallucination rate). Outputs per-question CSV and summary CSV.

## Known breakage

- **`eval/run_eval.py` is currently broken.** It does `from app import ... VLLM_URL` (line 39) and calls `VLLM_URL` in `generate_answer`, but the Ollama Cloud refactor renamed that constant to `LLM_URL` and removed `VLLM_URL` from `app.py`. The import now raises `ImportError` before any evaluation runs. To fix, update the eval script to import `LLM_URL` and send the **chat** payload format (`messages=[...]` against `/v1/chat/completions`) — `generate_answer` still posts the old vLLM `prompt=...` body to `/v1/completions`, which the configured Ollama Cloud endpoint does not serve.

## Key coupling to be aware of

- `eval/run_eval.py` imports the embedding model singleton and config constants from `app.py` at module level. This is why renaming a config constant in `app.py` breaks eval (see above). The embedding model loads on import, so running eval or any script that imports `app` requires the model to be cached in `~/.cache/huggingface/`.

## Environment variables

All have defaults; see `.env.example`. Note the **code defaults differ from the shipped `.env.example`**: `app.py` defaults to local Ollama (`http://localhost:11434/v1/chat/completions`, `phi3:mini`), but `.env.example` configures **Ollama Cloud** (`https://ollama.com/v1/chat/completions`, `gemma3:27b-cloud`) — the intended production backend. The ones that change behavior most:
- `LLM_URL` — endpoint for the chat API (code default: local Ollama; `.env.example`: Ollama Cloud). Also accepts `VLLM_URL` as a fallback name.
- `MODEL_NAME` — model name sent to the LLM endpoint (code default: `phi3:mini`; `.env.example`: `gemma3:27b-cloud`)
- `LLM_API_KEY` — API key for cloud providers, sent as `Authorization: Bearer` (also accepts `OLLAMA_API_KEY` as a fallback name). Required for Ollama Cloud.
- `EMBEDDING_DEVICE` — `cuda` or `cpu` (Docker forces `cpu`)
- `CHUNK_SIZE`, `CHUNK_OVERLAP`, `RETRIEVER_K` — RAG parameters

`generate_stream` picks the payload shape from the URL: `/v1/chat/completions` → OpenAI/Ollama chat format; anything else → vLLM `/v1/completions` format. Switching backends is purely a `LLM_URL`/`MODEL_NAME`/`LLM_API_KEY` change.
