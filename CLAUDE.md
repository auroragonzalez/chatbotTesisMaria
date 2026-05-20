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

# Run evaluation benchmark
python eval/run_eval.py --models phi3 salamandra mistral qwen
```

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

**Corpus format**: plain-text Spanish files organized by festival and topic (`faq.txt`, `horarios.txt`, `accesos.txt`, `transporte.txt`). One idea per paragraph or Q&A format.

**Evaluation** (`eval/`): `qa_benchmark.json` (17 questions across phases + out-of-scope hallucination checks) + `run_eval.py` (ROUGE-L, BERTScore F1 Spanish, latency, hallucination rate). Outputs per-question CSV and summary CSV.

## Key coupling to be aware of

- `eval/run_eval.py` imports the embedding model singleton and config constants from `app.py` at module level. Changing variable names in `app.py` (e.g., `VLLM_URL` → `LLM_URL`) can break the eval script silently.
- The embedding model loads on import, so running eval or any script that imports `app` requires the model to be cached in `~/.cache/huggingface/`.

## Environment variables

All have defaults; see `.env.example`. The ones that change behavior most:
- `LLM_URL` — endpoint for the chat API (default: Ollama local at `http://localhost:11434/v1/chat/completions`)
- `MODEL_NAME` — model name sent to the LLM endpoint (default: `phi3:mini`)
- `LLM_API_KEY` — API key for cloud providers (sent as `Authorization: Bearer`)
- `EMBEDDING_DEVICE` — `cuda` or `cpu`
- `CHUNK_SIZE`, `CHUNK_OVERLAP`, `RETRIEVER_K` — RAG parameters
