"""
Fusiona respuestas + ROUGE/BERT + RAGAS en un Excel final con:
  - hoja 'detalle'  : una fila por pregunta con todas las métricas
  - hoja 'resumen'  : medias globales y desglosadas por phase / difficulty

Uso:  python eval/merge_results.py
"""
import json
from pathlib import Path
from datetime import date
import pandas as pd

E = Path(__file__).parent
answers = json.loads((E / "festai_eval_answers.json").read_text(encoding="utf-8"))
lexical = {x["id"]: x for x in json.loads((E / "festai_eval_lexical.json").read_text(encoding="utf-8"))}
ragas_p = E / "festai_eval_ragas.json"
ragas   = {x["id"]: x for x in json.loads(ragas_p.read_text(encoding="utf-8"))} if ragas_p.exists() else {}
# context_precision recalculado aparte (baja concurrencia) -> tiene prioridad
cp_p = E / "festai_eval_cp.json"
if cp_p.exists():
    for x in json.loads(cp_p.read_text(encoding="utf-8")):
        if x.get("context_precision") is not None and x["id"] in ragas:
            ragas[x["id"]]["context_precision"] = x["context_precision"]

NO_INFO = ["no tengo", "no dispongo", "no está en el contexto", "no aparece",
           "no hay información", "no se especifica", "no se menciona", "no figura",
           "no tengo información", "no se proporciona", "no se indica"]

rows = []
for r in answers:
    rid = r["id"]
    ans_l = (r["answer"] or "").lower()
    out_of_corpus = str(r.get("answerable_from_corpus", "")).strip().lower() in ("no", "false", "0")
    said_no_info = any(p in ans_l for p in NO_INFO)
    lx = lexical.get(rid, {})
    rg = ragas.get(rid, {})
    rows.append({
        "id": rid, "phase": r.get("phase"), "cat": r.get("cat"),
        "difficulty": r.get("difficulty"), "type": r.get("type"),
        "answerable_from_corpus": r.get("answerable_from_corpus"),
        "question": r["question"],
        "expected_answer": r.get("expected_answer", ""),
        "answer": r["answer"],
        "retrieved_files": r.get("retrieved_files", ""),
        "evidence_file": r.get("evidence_file", ""),
        "latency_s": r.get("latency_s"),
        "rouge_l": lx.get("rouge_l"),
        "bertscore_f1": lx.get("bertscore_f1"),
        "faithfulness": rg.get("faithfulness"),
        "answer_relevancy": rg.get("answer_relevancy"),
        "context_precision": rg.get("context_precision"),
        "context_recall": rg.get("context_recall"),
        "out_of_corpus": out_of_corpus,
        "said_no_info": said_no_info,
        # alucinación: pregunta fuera de corpus pero el modelo NO admitió desconocer
        "hallucinated": out_of_corpus and not said_no_info,
    })

df = pd.DataFrame(rows)

METRICS = ["rouge_l", "bertscore_f1", "faithfulness", "answer_relevancy",
           "context_precision", "context_recall", "latency_s"]

def means(sub):
    d = {"n": len(sub)}
    for m in METRICS:
        v = pd.to_numeric(sub[m], errors="coerce").dropna()
        d[m] = round(v.mean(), 4) if len(v) else None
    return d

summary = [{"grupo": "GLOBAL", **means(df)}]
for col in ("phase", "difficulty"):
    for val, sub in df.groupby(col):
        summary.append({"grupo": f"{col}={val}", **means(sub)})

# Métricas de alucinación (solo si el benchmark tiene preguntas fuera de corpus)
ooc = df[df["out_of_corpus"]]
halluc_rate = round(ooc["hallucinated"].mean(), 4) if len(ooc) else None
if len(ooc):
    summary.append({"grupo": f"hallucination_rate (n_fuera_corpus={len(ooc)})",
                    "n": len(ooc), "faithfulness": halluc_rate})

dfsum = pd.DataFrame(summary)

out_xlsx = E.parent / "questions" / f"festai_eval_results_{date.today().isoformat()}.xlsx"
with pd.ExcelWriter(out_xlsx, engine="openpyxl") as w:
    df.to_excel(w, sheet_name="detalle", index=False)
    dfsum.to_excel(w, sheet_name="resumen", index=False)

print("=== RESUMEN GLOBAL ===")
g = summary[0]
for m in METRICS:
    print(f"  {m:18s}: {g[m]}")
if len(ooc):
    print(f"  hallucination_rate: {halluc_rate}  (sobre {len(ooc)} preguntas fuera de corpus)")
print(f"\nExcel guardado en: {out_xlsx}")
