"""
Agrega el panel de jueces RAGAS (LLM-as-a-jury).

Lee un festai_eval_ragas_<slug>.json por juez, y produce:
  - medias globales por juez y por métrica
  - media del JURADO (promedio entre jueces, por pregunta -> media global)
  - concordancia inter-juez: desviación estándar media entre jueces y
    correlación de Pearson media entre pares de jueces

Salida: questions/festai_eval_jury.xlsx  +  eval/festai_eval_jury.json (por pregunta)

Uso:  python eval/aggregate_jury.py  [slug1 slug2 ...]
"""
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd

E = Path(__file__).parent
METRICS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

# Jueces del panel (slug -> etiqueta legible)
DEFAULT = {
    "gemma3-12b":           "gemma3:12b (Gemma)",
    "ministral-3-14b":      "ministral-3:14b (Mistral)",
    "mistral-large-3-675b": "mistral-large-3:675b (Mistral)",
}

slugs = sys.argv[1:] or list(DEFAULT.keys())
judges = {}
for s in slugs:
    p = E / f"festai_eval_ragas_{s}.json"
    if not p.exists():
        print(f"AVISO: falta {p.name}, se omite")
        continue
    judges[s] = {x["id"]: x for x in json.loads(p.read_text(encoding="utf-8"))}
label = {s: DEFAULT.get(s, s) for s in judges}
print(f"Jueces en el panel: {list(judges)}")

ids = sorted(set().union(*[set(d) for d in judges.values()]))

# Por pregunta: valores de cada juez + media del jurado
per_q = []
for i in ids:
    row = {"id": i}
    for m in METRICS:
        vals = []
        for s in judges:
            v = judges[s].get(i, {}).get(m)
            row[f"{m}__{s}"] = v
            if v is not None:
                vals.append(v)
        row[f"{m}__jury"] = round(float(np.mean(vals)), 4) if vals else None
    per_q.append(row)
dfq = pd.DataFrame(per_q)
(E / "festai_eval_jury.json").write_text(
    json.dumps([{"id": r["id"], **{f"{m}": r[f"{m}__jury"] for m in METRICS}} for r in per_q],
               ensure_ascii=False, indent=2), encoding="utf-8")

def col_mean(col):
    v = pd.to_numeric(dfq[col], errors="coerce").dropna()
    return round(v.mean(), 4) if len(v) else None

# Tabla de medias globales: una fila por juez + fila JURADO
summary = []
for s in judges:
    summary.append({"juez": label[s], **{m: col_mean(f"{m}__{s}") for m in METRICS}})
summary.append({"juez": "JURADO (media del panel)", **{m: col_mean(f"{m}__jury") for m in METRICS}})
dfsum = pd.DataFrame(summary)

# Concordancia inter-juez:
#  - sigma medio entre jueces por métrica (dispersión por pregunta, promediada)
#  - correlación de Pearson media entre pares de jueces
agree = []
slist = list(judges)
for m in METRICS:
    cols = [f"{m}__{s}" for s in slist]
    sub = dfq[cols].apply(pd.to_numeric, errors="coerce")
    std_per_q = sub.std(axis=1, ddof=0)               # sigma entre jueces, por pregunta
    mean_std = round(std_per_q.mean(), 4)
    # correlación media entre pares
    corrs = []
    for a in range(len(slist)):
        for b in range(a + 1, len(slist)):
            pair = sub[[cols[a], cols[b]]].dropna()
            if len(pair) > 2 and pair.iloc[:, 0].std() > 0 and pair.iloc[:, 1].std() > 0:
                corrs.append(pair.iloc[:, 0].corr(pair.iloc[:, 1]))
    mean_corr = round(float(np.mean(corrs)), 4) if corrs else None
    agree.append({"metric": m, "sigma_medio_entre_jueces": mean_std,
                  "corr_media_pares": mean_corr})
dfagree = pd.DataFrame(agree)

out = E.parent / "questions" / "festai_eval_jury.xlsx"
with pd.ExcelWriter(out, engine="openpyxl") as w:
    dfsum.to_excel(w, sheet_name="medias", index=False)
    dfagree.to_excel(w, sheet_name="concordancia", index=False)
    dfq.to_excel(w, sheet_name="por_pregunta", index=False)

pd.set_option("display.width", 200)
print("\n=== MEDIAS POR JUEZ Y JURADO ===")
print(dfsum.to_string(index=False))
print("\n=== CONCORDANCIA INTER-JUEZ ===")
print(dfagree.to_string(index=False))
print(f"\nGuardado: {out}")
