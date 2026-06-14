"""ROUGE-L + BERTScore F1 vs ground truth sobre las 80 respuestas (paso 1)."""
import json
from pathlib import Path
from rouge_score import rouge_scorer
from bert_score import score as bscore

ANS = Path(__file__).parent / "festai_eval_answers.json"
OUT = Path(__file__).parent / "festai_eval_lexical.json"

rows = json.loads(ANS.read_text(encoding="utf-8"))
scored = [r for r in rows if str(r.get("expected_answer", "")).strip()]
print(f"Filas con ground truth: {len(scored)}/{len(rows)}")

scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
preds = [r["answer"] for r in scored]
refs  = [r["expected_answer"] for r in scored]

rouge = [scorer.score(ref, pred)["rougeL"].fmeasure for pred, ref in zip(preds, refs)]
print("Calculando BERTScore (es)...")
_, _, F = bscore(preds, refs, lang="es", verbose=False)
bert = F.tolist()

out = [{"id": r["id"], "rouge_l": round(rg, 4), "bertscore_f1": round(bf, 4)}
       for r, rg, bf in zip(scored, rouge, bert)]
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"ROUGE-L medio     : {sum(rouge)/len(rouge):.4f}")
print(f"BERTScore F1 medio: {sum(bert)/len(bert):.4f}")
print(f"Guardado en {OUT}")
