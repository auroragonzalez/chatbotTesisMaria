"""
Agrega las métricas del benchmark de 80 preguntas para las tablas del paper.
Une answers + lexical + ragas + (phase, corpus_layer del xlsx) y produce:
  - Tabla 1: Overall + por fase (Pre/During/Post)
  - Tabla 2: por capa de corpus (Festival / Turismo-Destino) + robustez
Métricas de referencia (ROUGE-L, BERTScore, context_precision/recall) se
promedian sobre los ítems con ground truth; faithfulness/answer_relevancy sobre
los ítems evaluados por RAGAS.
Uso:  python eval/aggregate_paper_tables.py [ragas_json]
"""
import json, sys
from pathlib import Path
import pandas as pd

E = Path(__file__).parent
XLSX = E.parent / "questions" / "80_preguntas_festai_ground_truth_with_evidence.xlsx"
ragas_file = Path(sys.argv[1]) if len(sys.argv) > 1 else E / "festai_eval_ragas.json"

meta = pd.read_excel(XLSX)[["id", "phase", "corpus_layer", "difficulty"]].set_index("id")
answers = {r["id"]: r for r in json.loads((E / "festai_eval_answers.json").read_text("utf-8"))}
lexical = {r["id"]: r for r in json.loads((E / "festai_eval_lexical.json").read_text("utf-8"))}
ragas   = {r["id"]: r for r in json.loads(ragas_file.read_text("utf-8"))}
# context_precision recalculado a baja concurrencia tiene prioridad (evita NaN)
cp_file = E / "festai_eval_cp.json"
if cp_file.exists():
    for x in json.loads(cp_file.read_text("utf-8")):
        if x.get("context_precision") is not None and x["id"] in ragas:
            ragas[x["id"]]["context_precision"] = x["context_precision"]

rows = []
for rid, m in meta.iterrows():
    lx, rg = lexical.get(rid, {}), ragas.get(rid, {})
    rows.append({
        "id": rid, "phase": m["phase"], "layer": m["corpus_layer"], "difficulty": m["difficulty"],
        "latency_s": (answers.get(rid) or {}).get("latency_s"),
        "rouge_l": lx.get("rouge_l"), "bertscore_f1": lx.get("bertscore_f1"),
        "faithfulness": rg.get("faithfulness"), "answer_relevancy": rg.get("answer_relevancy"),
        "context_precision": rg.get("context_precision"), "context_recall": rg.get("context_recall"),
    })
df = pd.DataFrame(rows)
MET = ["faithfulness", "answer_relevancy", "context_precision", "context_recall",
       "rouge_l", "bertscore_f1", "latency_s"]

def line(name, sub):
    vals = {m: round(pd.to_numeric(sub[m], errors="coerce").dropna().mean(), 3) for m in MET}
    n = pd.to_numeric(sub["faithfulness"], errors="coerce").notna().sum()
    print(f"{name:22} n_gt={n:2}  " + " ".join(f"{m.split('_')[0][:5]}={vals[m]}" for m in MET))

print("\n===== TABLA 1: Overall + por fase (solo ítems con ground truth) =====")
gt = df[df["faithfulness"].notna()]
line("Overall", gt)
for ph, lab in [("PRE", "Pre"), ("DURANTE", "During"), ("POST", "Post")]:
    line(lab, gt[gt["phase"] == ph])

print("\n===== TABLA 2: por capa de corpus =====")
for layer in ["Festival", "Turismo/Destino"]:
    line(layer, gt[gt["layer"] == layer])
print("\n--- Robustez (difficulty=Robustez, todas las columnas disponibles) ---")
line("Robustez", df[df["difficulty"] == "Robustez"])
