"""
Barrido de k (RETRIEVER_K): equilibrio recall <-> precision de la RECUPERACIÓN.

Usa la columna `evidence_file` del benchmark como verdad de referencia (el archivo
de corpus que contiene la respuesta). Para cada pregunta recupera los top-K_MAX
chunks UNA vez y calcula, por cada k:
  - Recall@k  (hit@k, nivel archivo): el evidence_file aparece en el top-k
  - Precision@k (nivel chunk): fracción de los k chunks que son del evidence_file
  - F1@k
  - MRR (rango del primer chunk del evidence_file)  -- independiente de k

Es 100% local (solo búsqueda por embeddings), sin llamadas al LLM.
Excluye las preguntas cuyo evidence_file no está ingestado como .txt.

Uso:  python eval/sweep_k.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from langchain_community.vectorstores import Chroma
from app import CHROMA_DIR, embedding_model

K_MAX = 30
FESTIVAL = "warm_up"
XLSX = Path(__file__).parent.parent / "questions" / "80_preguntas_festai_ground_truth_with_evidence.xlsx"
OUT = Path(__file__).parent.parent / "questions" / "festai_k_sweep.xlsx"

db = Chroma(collection_name=FESTIVAL, persist_directory=str(CHROMA_DIR),
            embedding_function=embedding_model)

ingested = {p.name for p in (Path(__file__).parent.parent / "festival_txts_big" / "warm_up").rglob("*.txt")}

df = pd.read_excel(XLSX)
df["evidence_file"] = df["evidence_file"].astype(str).str.strip()
valid = df[df["evidence_file"].isin(ingested)].copy()
excluded = len(df) - len(valid)
print(f"Preguntas: {len(df)} | con evidence_file ingestado: {len(valid)} | excluidas: {excluded}")

# Recupera top-K_MAX una vez por pregunta -> lista ordenada de basenames
retrievals = []  # (evidence_file, [file_por_chunk...])
for _, r in valid.iterrows():
    docs = db.similarity_search(r["question"], k=K_MAX)
    files = [Path(d.metadata.get("source", "?")).name for d in docs]
    retrievals.append((r["evidence_file"], files))

rows = []
for k in range(1, K_MAX + 1):
    rec = prec = 0.0
    for ev, files in retrievals:
        topk = files[:k]
        hit = ev in topk
        rec += 1.0 if hit else 0.0
        prec += sum(1 for f in topk if f == ev) / k
    n = len(retrievals)
    rec /= n
    prec /= n
    f1 = (2 * rec * prec / (rec + prec)) if (rec + prec) else 0.0
    rows.append({"k": k, "recall@k": round(rec, 4), "precision@k": round(prec, 4),
                 "f1@k": round(f1, 4)})

# MRR (independiente de k)
mrr = 0.0
for ev, files in retrievals:
    rank = next((i + 1 for i, f in enumerate(files) if f == ev), None)
    mrr += (1.0 / rank) if rank else 0.0
mrr /= len(retrievals)

sweep = pd.DataFrame(rows)
with pd.ExcelWriter(OUT, engine="openpyxl") as w:
    sweep.to_excel(w, sheet_name="sweep", index=False)
    pd.DataFrame([{"n_preguntas": len(valid), "excluidas_evidence_no_ingestada": excluded,
                   "MRR": round(mrr, 4)}]).to_excel(w, sheet_name="meta", index=False)

print(f"\nMRR (rango medio del evidence_file): {mrr:.4f}\n")
print("k  | recall@k | precision@k | f1@k")
for _, r in sweep.iterrows():
    star = "  <- en uso" if int(r["k"]) in (4, 8, 15, 25) else ""
    print(f"{int(r['k']):2d} |  {r['recall@k']:.3f}  |   {r['precision@k']:.3f}    | {r['f1@k']:.3f}{star}")
print(f"\nGuardado en {OUT}")
