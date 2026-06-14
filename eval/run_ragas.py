"""
Paso 2 del benchmark: métricas RAGAS sobre las respuestas generadas en el paso 1.

Se ejecuta en el venv AISLADO .venv-eval (ragas 0.2.15 + langchain 0.2.x),
para no tocar el stack langchain 1.x de la app.

Juez LLM: gemma3:27b vía Ollama Cloud (OpenAI-compatible).
Embeddings: intfloat/multilingual-e5-base (CPU).

Métricas: faithfulness, answer_relevancy, context_precision, context_recall.
(Las dos de contexto requieren ground truth -> solo filas con expected_answer.)

Uso:
    OLLAMA_API_KEY=... python eval/run_ragas.py
"""
import os, sys, json
from pathlib import Path

os.environ.setdefault("RAGAS_DO_NOT_TRACK", "true")

ANS_JSON = Path(__file__).parent / "festai_eval_answers.json"
OUT_JSON = Path(__file__).parent / "festai_eval_ragas.json"

API_KEY = os.environ.get("LLM_API_KEY") or os.environ.get("OLLAMA_API_KEY")
BASE_URL = os.environ.get("LLM_BASE_URL", "https://ollama.com/v1")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemma3:27b")
EMB_MODEL = "intfloat/multilingual-e5-base"

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from ragas import evaluate
from ragas.dataset_schema import EvaluationDataset, SingleTurnSample
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig


def build_judge():
    chat = ChatOpenAI(model=JUDGE_MODEL, base_url=BASE_URL, api_key=API_KEY,
                      temperature=0, timeout=180, max_retries=2)
    return LangchainLLMWrapper(chat)


def main():
    rows = json.loads(ANS_JSON.read_text(encoding="utf-8"))
    # Solo filas con ground truth (las métricas de contexto lo requieren)
    scored = [r for r in rows if str(r.get("expected_answer", "")).strip()]
    print(f"Filas totales: {len(rows)} | con ground truth (evaluadas): {len(scored)}")

    samples = [SingleTurnSample(
        user_input=r["question"],
        response=r["answer"],
        retrieved_contexts=r["retrieved_contexts"],
        reference=r["expected_answer"],
    ) for r in scored]
    dataset = EvaluationDataset(samples=samples)

    judge = build_judge()
    emb = LangchainEmbeddingsWrapper(HuggingFaceEmbeddings(
        model_name=EMB_MODEL, model_kwargs={"device": "cpu"}))

    metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
    workers = int(os.environ.get("RAGAS_WORKERS", "12"))
    run_cfg = RunConfig(max_workers=workers, timeout=180, max_retries=2)

    print(f"Juez: {JUDGE_MODEL} @ {BASE_URL}  | métricas: {[m.name for m in metrics]}")
    result = evaluate(dataset=dataset, metrics=metrics, llm=judge, embeddings=emb,
                      run_config=run_cfg, raise_exceptions=False)

    dfres = result.to_pandas()
    # Asocia por id para mezclar luego
    out = []
    for r, (_, mr) in zip(scored, dfres.iterrows()):
        out.append({
            "id": r["id"],
            "faithfulness":      _num(mr.get("faithfulness")),
            "answer_relevancy":  _num(mr.get("answer_relevancy")),
            "context_precision": _num(mr.get("context_precision")),
            "context_recall":    _num(mr.get("context_recall")),
        })
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== MEDIAS RAGAS ===")
    for m in metrics:
        vals = [o[m.name] for o in out if o[m.name] is not None]
        avg = sum(vals)/len(vals) if vals else float("nan")
        print(f"  {m.name:18s}: {avg:.4f}  (n={len(vals)})")
    print(f"\nGuardado en {OUT_JSON}")


def _num(x):
    try:
        import math
        f = float(x)
        return None if math.isnan(f) else round(f, 4)
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    main()
