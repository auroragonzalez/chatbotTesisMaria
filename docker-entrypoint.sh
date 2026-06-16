#!/bin/sh
# ──────────────────────────────────────────────────────────────────────
# Entrypoint del contenedor FestAI.
#
# Garantiza que el índice Chroma servido es coherente con el corpus.
# Toda la configuración (DATA_DIR, CHROMA_DIR, RAG, modelo...) vive en
# constants.py; aquí solo decidimos si hay que (re)ingestar.
#
#   - Si no existe el índice (chroma.sqlite3) -> ingesta automática.
#   - Si INGEST_ON_START=1 -> fuerza una reconstrucción aunque ya exista.
#   - En caso contrario, usa el chroma_db existente tal cual.
#
# CHROMA_DIR=./chroma_db en constants.py y WORKDIR=/app => /app/chroma_db.
# ──────────────────────────────────────────────────────────────────────
set -e

CHROMA_SQLITE="/app/chroma_db/chroma.sqlite3"

needs_ingest=0
if [ "${INGEST_ON_START:-0}" = "1" ]; then
    echo "[entrypoint] INGEST_ON_START=1 -> se forzará la reconstrucción del corpus."
    needs_ingest=1
elif [ ! -f "$CHROMA_SQLITE" ]; then
    echo "[entrypoint] No se encontró $CHROMA_SQLITE -> ingesta inicial."
    needs_ingest=1
fi

if [ "$needs_ingest" = "1" ]; then
    echo "[entrypoint] Reconstruyendo Chroma (DATA_DIR según constants.py) ..."
    python app.py --ingest
fi

echo "[entrypoint] Lanzando FestAI ..."
exec python app.py "$@"
