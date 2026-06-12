"""
FestGPT — Evaluación comparativa de modelos LLM
================================================
Llama al mismo endpoint que la app (LLM_URL): detecta automáticamente
formato chat (/v1/chat/completions, Ollama Cloud/OpenAI) o completions (vLLM).
El nombre de modelo se envía tal cual al endpoint; los alias de abajo son
atajos opcionales que se expanden a nombres HuggingFace (útiles con vLLM).

Ejecutar:
    python eval/run_eval.py                          # evalúa MODEL_NAME (config de app.py)
    python eval/run_eval.py --models gemma3:27b-cloud
    python eval/run_eval.py --models phi3 salamandra mistral  # compara varios (vLLM)

Alias opcionales (alias → nombre HuggingFace, para backends vLLM):
    phi3        microsoft/Phi-3-mini-4k-instruct
    salamandra  BSC-LT/salamandra-7b-instruct
    mistral     mistralai/Mistral-7B-Instruct-v0.3
    llama3      meta-llama/Llama-3.1-8B-Instruct
    qwen        Qwen/Qwen2.5-7B-Instruct
    tinyllama   TinyLlama/TinyLlama-1.1B-Chat-v1.0

Salida:
    eval/results_<timestamp>.csv   ← métricas por pregunta
    eval/summary_<timestamp>.csv   ← media por modelo y fase

Requisitos adicionales:
    pip install rouge-score bert-score ragas
"""

import os
import sys
import json
import time
import argparse
import csv
import requests
from pathlib import Path
from datetime import datetime

# Añadir la raíz del proyecto al path para importar de app.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import (
    CHROMA_DIR, EMBEDDING_MODEL, EMBEDDING_DEVICE,
    RETRIEVER_K, TEMPERATURE, LLM_URL, LLM_API_KEY, MODEL_NAME,
    embedding_model, get_context, build_prompt, PHASE_PROMPTS,
)

# ─────────────────────────────────────────────
# ALIAS DE MODELOS
# ─────────────────────────────────────────────

MODEL_ALIASES = {
    "phi3":       "microsoft/Phi-3-mini-4k-instruct",
    "salamandra": "BSC-LT/salamandra-7b-instruct",
    "mistral":    "mistralai/Mistral-7B-Instruct-v0.3",
    "llama3":     "meta-llama/Llama-3.1-8B-Instruct",
    "qwen":       "Qwen/Qwen2.5-7B-Instruct",
    "tinyllama":  "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
}

BENCHMARK_PATH = Path(__file__).parent / "qa_benchmark.json"
FESTIVAL        = "warm_up"   # festival sobre el que está construido el benchmark


# ─────────────────────────────────────────────
# MÉTRICAS
# ─────────────────────────────────────────────

def rouge_l(prediction: str, reference: str) -> float:
    """ROUGE-L entre predicción y referencia esperada."""
    from rouge_score import rouge_scorer
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    return scorer.score(reference, prediction)["rougeL"].fmeasure


def bertscore_f1(predictions: list[str], references: list[str]) -> list[float]:
    """BERTScore F1 en bloque (más eficiente que llamada por llamada)."""
    from bert_score import score as bscore
    _, _, F = bscore(predictions, references, lang="es", verbose=False)
    return F.tolist()


def hallucination_rate(answers: list[str], expected_no_info: list[bool]) -> float:
    """
    Tasa de alucinación: fracción de preguntas fuera de corpus donde el modelo
    NO respondió 'No tengo esa información' (o equivalente).
    """
    no_info_phrases = [
        "no tengo esa información",
        "no dispongo de esa información",
        "no está en el contexto",
        "no tengo información",
    ]
    hallucinated = 0
    total = sum(expected_no_info)
    if total == 0:
        return 0.0
    for ans, is_out_of_scope in zip(answers, expected_no_info):
        if is_out_of_scope:
            ans_lower = ans.lower()
            if not any(phrase in ans_lower for phrase in no_info_phrases):
                hallucinated += 1
    return hallucinated / total


# ─────────────────────────────────────────────
# GENERACIÓN (llamada al endpoint LLM con el modelo activo)
# ─────────────────────────────────────────────

def generate_answer(question: str, phase: str, model_name: str, max_tokens: int = 256) -> tuple[str, float]:
    """
    Llama al endpoint LLM (LLM_URL) y devuelve (respuesta, latencia_segundos).
    Detecta el formato igual que app.generate_stream: /v1/chat/completions
    (Ollama/OpenAI) vs /v1/completions (vLLM), sin streaming.
    """
    context = get_context(question, FESTIVAL)
    prompt  = build_prompt(context, question, phase)

    is_chat_api = "/chat/completions" in LLM_URL
    if is_chat_api:
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": TEMPERATURE,
            "stream": False,
        }
    else:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": TEMPERATURE,
            "stream": False,
        }

    headers = {}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    t0 = time.time()
    try:
        resp = requests.post(LLM_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        choice = resp.json()["choices"][0]
        answer = (choice["message"]["content"] if is_chat_api else choice["text"]).strip()
    except Exception as e:
        answer = f"[ERROR: {e}]"
    latency = time.time() - t0
    return answer, latency


# ─────────────────────────────────────────────
# EVALUACIÓN PRINCIPAL
# ─────────────────────────────────────────────

def run_evaluation(model_aliases: list[str]) -> None:
    benchmark = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = Path(__file__).parent / f"results_{timestamp}.csv"
    summary_path = Path(__file__).parent / f"summary_{timestamp}.csv"

    all_rows = []

    for alias in model_aliases:
        model_name = MODEL_ALIASES.get(alias, alias)
        print(f"\n{'='*60}")
        print(f"Evaluando: {alias} → {model_name}")
        print(f"{'='*60}")

        answers   = []
        refs      = []
        latencies = []
        out_of_scope_flags = []

        for item in benchmark:
            q     = item["question"]
            ref   = item["expected"]
            phase = item["phase"].capitalize()
            if phase not in PHASE_PROMPTS:
                # Normaliza variantes de fase
                phase = {"pre": "Pre-festival", "durante": "Durante", "post": "Post-festival"}.get(
                    item["phase"], "Pre-festival"
                )

            print(f"  [{item['id']}] {q[:60]}...")
            answer, latency = generate_answer(q, phase, model_name)
            print(f"         → {answer[:80]}... ({latency:.1f}s)")

            answers.append(answer)
            refs.append(ref)
            latencies.append(latency)
            out_of_scope_flags.append(item.get("category") == "fuera_de_corpus")

        # ROUGE-L por pregunta
        rouge_scores = [rouge_l(a, r) for a, r in zip(answers, refs)]

        # BERTScore en bloque
        print("  Calculando BERTScore...")
        bert_scores = bertscore_f1(answers, refs)

        # Tasa de alucinación global del modelo
        halluc = hallucination_rate(answers, out_of_scope_flags)

        for i, item in enumerate(benchmark):
            all_rows.append({
                "model_alias":    alias,
                "model_name":     model_name,
                "id":             item["id"],
                "phase":          item["phase"],
                "category":       item["category"],
                "question":       item["question"],
                "expected":       item["expected"],
                "answer":         answers[i],
                "rouge_l":        round(rouge_scores[i], 4),
                "bertscore_f1":   round(bert_scores[i], 4),
                "latency_s":      round(latencies[i], 2),
                "out_of_scope":   out_of_scope_flags[i],
                "hallucination_rate": round(halluc, 4),
            })

    # Guardar resultados por pregunta
    if all_rows:
        with open(results_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nResultados por pregunta → {results_path}")

    # Resumen por modelo × fase
    from collections import defaultdict
    summary = defaultdict(lambda: {"rouge_l": [], "bertscore_f1": [], "latency_s": []})
    for row in all_rows:
        key = (row["model_alias"], row["phase"])
        summary[key]["rouge_l"].append(row["rouge_l"])
        summary[key]["bertscore_f1"].append(row["bertscore_f1"])
        summary[key]["latency_s"].append(row["latency_s"])

    summary_rows = []
    for (alias, phase), vals in sorted(summary.items()):
        n = len(vals["rouge_l"])
        summary_rows.append({
            "model":          alias,
            "phase":          phase,
            "n_questions":    n,
            "rouge_l_mean":   round(sum(vals["rouge_l"]) / n, 4),
            "bertscore_mean": round(sum(vals["bertscore_f1"]) / n, 4),
            "latency_mean_s": round(sum(vals["latency_s"]) / n, 2),
        })

    if summary_rows:
        with open(summary_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
            writer.writeheader()
            writer.writerows(summary_rows)
        print(f"Resumen por modelo/fase  → {summary_path}")

    # Imprimir tabla rápida en consola
    print("\n── RESUMEN ──────────────────────────────────────────────")
    print(f"{'Modelo':<15} {'Fase':<15} {'ROUGE-L':>8} {'BERTScore':>10} {'Latencia':>10}")
    print("─" * 62)
    for r in summary_rows:
        print(f"{r['model']:<15} {r['phase']:<15} {r['rouge_l_mean']:>8.4f} {r['bertscore_mean']:>10.4f} {r['latency_mean_s']:>9.2f}s")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FestGPT — evaluación comparativa de modelos")
    parser.add_argument(
        "--models",
        nargs="+",
        default=[MODEL_NAME],
        help=f"Modelos a evaluar (nombre directo o alias). Alias disponibles: {', '.join(MODEL_ALIASES)}",
    )
    args = parser.parse_args()
    run_evaluation(args.models)
