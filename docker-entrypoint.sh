#!/bin/sh
# ──────────────────────────────────────────────────────────────────────
# Entrypoint del contenedor FestAI.
#
# Garantiza que el índice Chroma servido es coherente con el corpus
# apuntado por DATA_DIR (en producción: ./festival_txts_big).
#
#   - Si no existe el índice (chroma.sqlite3) -> ingesta automática.
#   - Si INGEST_ON_START=1 -> fuerza una reconstrucción aunque ya exista.
#   - En caso contrario, usa el chroma_db existente tal cual.
# ──────────────────────────────────────────────────────────────────────
set -e

CHROMA_DIR="${CHROMA_DIR:-/app/chroma_db}"
DATA_DIR="${DATA_DIR:-./festival_txts_big}"
export CHROMA_DIR DATA_DIR

needs_ingest=0
if [ "${INGEST_ON_START:-0}" = "1" ]; then
    echo "[entrypoint] INGEST_ON_START=1 -> se forzará la reconstrucción del corpus."
    needs_ingest=1
elif [ ! -f "${CHROMA_DIR}/chroma.sqlite3" ]; then
    echo "[entrypoint] No se encontró ${CHROMA_DIR}/chroma.sqlite3 -> ingesta inicial."
    needs_ingest=1
fi

if [ "$needs_ingest" = "1" ]; then
    echo "[entrypoint] Reconstruyendo Chroma desde DATA_DIR=${DATA_DIR} ..."
    python app.py --ingest
fi

echo "[entrypoint] Lanzando FestAI (DATA_DIR=${DATA_DIR}, CHROMA_DIR=${CHROMA_DIR})"
exec python app.py "$@"
