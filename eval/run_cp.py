"""Re-ejecuta SOLO context_precision (las 72 con ground truth) con baja
concurrencia para evitar los NaN por saturación del run principal."""
import os, json, math
from pathlib import Path
os.environ.setdefault("RAGAS_DO_NOT_TRACK", "true")
from langchain_openai import ChatOpenAI
from ragas.dataset_schema import EvaluationDataset, SingleTurnSample
from ragas.metrics import context_precision
from ragas.llms import LangchainLLMWrapper
from ragas import evaluate
from ragas.run_config import RunConfig

E = Path(__file__).parent
rows = [r for r in json.load(open(E/"festai_eval_answers.json")) if str(r.get("expected_answer","")).strip()]
key = os.environ["LLM_API_KEY"]
judge = LangchainLLMWrapper(ChatOpenAI(model=os.environ.get("JUDGE_MODEL","gemma3:12b"),
        base_url="https://ollama.com/v1", api_key=key, temperature=0, timeout=180, max_retries=4))
ds = EvaluationDataset(samples=[SingleTurnSample(
        user_input=r["question"], response=r["answer"],
        retrieved_contexts=r["retrieved_contexts"], reference=r["expected_answer"]) for r in rows])
res = evaluate(dataset=ds, metrics=[context_precision], llm=judge,
        run_config=RunConfig(max_workers=4, timeout=180, max_retries=4), raise_exceptions=False)
df = res.to_pandas()
out = []
for r,(_,mr) in zip(rows, df.iterrows()):
    v = mr.get("context_precision")
    try: v = None if (v is None or math.isnan(float(v))) else round(float(v),4)
    except: v = None
    out.append({"id": r["id"], "context_precision": v})
(E/"festai_eval_cp.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
vals=[o["context_precision"] for o in out if o["context_precision"] is not None]
print(f"context_precision medio: {sum(vals)/len(vals):.4f} (n={len(vals)}/{len(out)})")
