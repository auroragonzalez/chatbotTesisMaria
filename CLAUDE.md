# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

FestAI is a RAG-based chatbot for music festivals (Gradio UI + LangChain + ChromaDB + external LLM). The entire application is a single-file Python app (`app.py`, ~400 lines). It is part of a PhD thesis targeting a 2026 special issue on LLMs for tourism.

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
# Build + run; reads .env (secrets only), mounts ./chroma_db and ./festival_txts_big; config in constants.py
docker compose up --build
```

The container runs the Gradio app on port 7860 with a healthcheck. It does **not** run `--ingest`; populate `chroma_db/` on the host first (the volume is bind-mounted) or exec the ingest command inside the container.

## Architecture

**Single-file app (`app.py`)** — also acts as a library imported by `eval/run_eval.py`. Key sections in order:

1. **Config**: non-secret settings imported from `constants.py` and re-exposed at module level; secrets (`LLM_API_KEY`, `HF_TOKEN`) read from the environment / `.env`. See "Configuration" below.
2. **Embeddings singleton** (line 144): `HuggingFaceEmbeddings` with `multilingual-e5-base` loads at **import time**, not lazily. This means any script that imports `app` pays the embedding model load cost immediately.
3. **Corpus ingestion** (`ingest_corpus`): loads `.txt` files via `DirectoryLoader`, splits with `RecursiveCharacterTextSplitter`, stores in Chroma with one **collection per festival** (collection name = folder name). Deletes and rebuilds the collection on each run.
4. **Retrieval** (`get_context`): similarity search returning top-k chunks from the festival's Chroma collection.
5. **Prompt construction** (`build_prompt`): assembles `SYSTEM_BASE` + **default assumptions** + phase instruction + retrieved context + user question. Three phases: Pre-festival, Durante, Post-festival. Default assumptions (single-festival use case): if the user names no festival, assume `FESTIVAL_DISPLAY_NAME` (WARM UP Estrella de Levante, from `constants.py`); if no year/edition is given, assume the current year (`datetime.now().year`, dynamic). `chat()` also defaults the festival to `DEFAULT_FESTIVAL` (`warm_up`) when none is selected.
6. **LLM streaming** (`generate_stream`): SSE-based streaming via `requests`. Auto-detects `/v1/chat/completions` (Ollama/OpenAI format) vs `/v1/completions` (vLLM format) based on the URL string. Supports `LLM_API_KEY` for cloud providers.
7. **Gradio UI**: `gr.Blocks` with festival dropdown (auto-populated from `festival_txts/` subdirectories), phase radio, and `gr.ChatInterface`.
8. **CLI**: argparse with `--ingest`, `--festival`, `--download-model`.

**Festival auto-detection**: `get_festivals()` scans `festival_txts/` for subdirectories at runtime. Adding a new festival is just creating a folder with `.txt` files and re-ingesting.

**Corpus format**: plain-text Spanish files organized by festival and topic (`faq.txt`, `horarios.txt`, `accesos.txt`, `transporte.txt`). One idea per paragraph or Q&A format. Ingestion globs `**/*.txt` recursively, so nested topic folders are fine.

**Two corpora**:
- `festival_txts/` — the committed corpus and the default `DATA_DIR`. Three festivals: `animal_sound`, `mar_de_musicas`, `warm_up`, each with the four canonical topic files.
- `festival_txts_big/` — an untracked, richer **warm_up-only** corpus (granular topic folders, plus `.csv`/`.jpg` assets and `.DS_Store` macOS junk). Its content is exposed as a single festival folder `festival_txts_big/warm_up/` (310 `.txt` across topic subfolders: `bandas_warmup`, `horarios_warmup`, `alojamientos_warmup`, `salida_laverdad_warmup_tema`, etc.). To use it, set `DATA_DIR=./festival_txts_big` and re-ingest `warm_up`; only `**/*.txt` is loaded (CSV/JPG ignored). This is the **active corpus** in the local `.env`. Note: ~36 files under `warm_up/warm_up/` were originally Mac OS Roman encoded and have been converted to UTF-8; `ingest_corpus` also sets `autodetect_encoding=True` as a safety net.

**Evaluation** (`eval/`): a **bilingual** benchmark pair — `qa_benchmark.json` (Spanish) and `qa_benchmark_en.json` (English), 17 questions each with identical `id`/`phase`/`category` (across phases + out-of-scope hallucination checks) — plus `run_eval.py` (ROUGE-L, BERTScore F1, latency, hallucination rate). Select the file with `--benchmark`; output CSVs are tagged with the benchmark stem. Hallucination detection recognizes "no info" phrasings in both languages. The app is bilingual: `SYSTEM_BASE` instructs the LLM to answer in the user's language (ES/EN), though the corpus itself is Spanish.

## Key coupling to be aware of

- `eval/run_eval.py` imports the embedding model singleton and config constants (`LLM_URL`, `LLM_API_KEY`, `MODEL_NAME`, etc.) from `app.py` at module level — so renaming a config constant in `app.py` breaks the eval import. (This already happened once: the Ollama Cloud refactor renamed `VLLM_URL`→`LLM_URL` and broke the eval `import` until fixed.) The embedding model loads on import, so running eval or any script that imports `app` requires the model to be cached in `~/.cache/huggingface/`.

## Configuration

Config is split in two:
- **`constants.py`** — single source of truth for **all non-secret settings** (`LLM_URL`, `MODEL_NAME`, `EMBEDDING_MODEL`, `EMBEDDING_DEVICE`, `CHROMA_DIR`, `DATA_DIR`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `RETRIEVER_K`, `MAX_TOKENS`, `TEMPERATURE`, `SERVER_PORT`, `CUDA_VISIBLE_DEVICES`). These are **plain Python constants, not env-overridable** — intentional, to keep deployment deterministic (this is what previously broke when Docker overrode `DATA_DIR` to the wrong corpus). `app.py` imports them and re-exposes them at module level (so `eval/run_eval.py`'s import of `LLM_URL`/`MODEL_NAME`/etc. still works). Paths are relative to the working dir (project root locally, `/app` in the container), so they're valid in both.
- **`.env`** (and `.env.example`) — **secrets only**: `LLM_API_KEY` (also accepts `OLLAMA_API_KEY`; sent as `Authorization: Bearer`) and `HF_TOKEN` (optional, for authenticated embedding-model download). Read via `os.getenv`. Loaded by `python-dotenv`.

To change the corpus, RAG params, model, or device, edit `constants.py` (not `.env`, not the Dockerfile/compose). After changing the corpus or chunking, re-ingest (`INGEST_ON_START=1 docker compose up --build`).

`generate_stream` picks the payload shape from the URL: `/v1/chat/completions` → OpenAI/Ollama chat format; anything else → vLLM `/v1/completions` format. Switching backends is a `constants.py` (`LLM_URL`/`MODEL_NAME`) + `.env` (`LLM_API_KEY`) change.
