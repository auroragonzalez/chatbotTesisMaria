"""
Paso 1 del benchmark de 80 preguntas (questions/*.xlsx).

- Genera la respuesta REAL del sistema con la configuración activa (.env).
- Captura los contextos recuperados (lista de chunks) para las métricas RAGAS.
- Calcula ROUGE-L y BERTScore F1 vs expected_answer.
- Guarda un JSON intermedio (para el paso RAGAS) y un Excel/CSV de resultados.

Uso:
    python eval/run_xlsx_answers.py
"""
import os, sys, json, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import requests
from langchain_community.vectorstores import Chroma

from app import (
    CHROMA_DIR, RETRIEVER_K, TEMPERATURE, MAX_TOKENS,
    LLM_URL, LLM_API_KEY, MODEL_NAME,
    embedding_model, build_prompt,
)

XLSX_IN   = Path(__file__).parent.parent / "questions" / "80_preguntas_festai_ground_truth_with_evidence.xlsx"
OUT_JSON  = Path(__file__).parent / "festai_eval_answers.json"
FESTIVAL  = "warm_up"

_db = Chroma(collection_name=FESTIVAL, persist_directory=str(CHROMA_DIR),
             embedding_function=embedding_model)


def retrieve(question: str):
    """Devuelve (lista_de_chunks, lista_de_archivos_fuente)."""
    docs = _db.similarity_search(question, k=RETRIEVER_K)
    chunks = [d.page_content for d in docs]
    files  = [Path(d.metadata.get("source", "?")).name for d in docs]
    return chunks, files


def generate(prompt: str) -> tuple[str, float]:
    """Llamada NO-streaming al LLM activo. Devuelve (respuesta, latencia_s)."""
    is_chat = "/chat/completions" in LLM_URL
    if is_chat:
        payload = {"model": MODEL_NAME,
                   "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE, "stream": False}
    else:
        payload = {"model": MODEL_NAME, "prompt": prompt,
                   "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE, "stream": False}
    headers = {"Content-Type": "application/json"}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"
    t0 = time.time()
    r = requests.post(LLM_URL, json=payload, headers=headers, timeout=180)
    r.raise_for_status()
    data = r.json()
    if is_chat:
        text = data["choices"][0]["message"]["content"]
    else:
        text = data["choices"][0].get("text", "")
    return (text or "").strip(), time.time() - t0


def main():
    df = pd.read_excel(XLSX_IN)
    phase_map = {"PRE": "Pre-festival", "DURANTE": "Durante", "DURING": "Durante",
                 "POST": "Post-festival"}
    rows = []
    n = len(df)
    for i, row in df.iterrows():
        q = str(row["question"]).strip()
        phase = phase_map.get(str(row.get("phase", "")).strip().upper(), "Pre-festival")
        chunks, files = retrieve(q)
        prompt = build_prompt("\n\n".join(chunks), q, phase)
        try:
            answer, lat = generate(prompt)
        except Exception as e:
            answer, lat = f"[ERROR: {e}]", 0.0
        exp = row.get("expected_answer")
        rows.append({
            "id": row.get("id"),
            "phase": row.get("phase"),
            "cat": row.get("cat"),
            "difficulty": row.get("difficulty"),
            "type": row.get("type"),
            "answerable_from_corpus": row.get("answerable_from_corpus"),
            "question": q,
            "expected_answer": "" if pd.isna(exp) else str(exp),
            "answer": answer,
            "retrieved_files": " | ".join(files),
            "retrieved_contexts": chunks,
            "evidence_file": row.get("evidence_file"),
            "latency_s": round(lat, 2),
        })
        print(f"[{i+1}/{n}] id={row.get('id')} lat={lat:5.1f}s  {q[:60]}", flush=True)

    OUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGuardado {len(rows)} respuestas en {OUT_JSON}")


if __name__ == "__main__":
    main()
