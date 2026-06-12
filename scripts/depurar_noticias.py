"""
Depuración semiautomática del corpus de noticias (La Verdad)
============================================================

Clasifica las noticias por categoría temática y propone una decisión de
INCLUSIÓN / EXCLUSIÓN / REVISIÓN, para construir el corpus RAG con criterios
explícitos y reproducibles (justificables metodológicamente en la tesis).

El proceso es SEMIautomático en dos fases:

  Fase 1 — clasificar (no toca el corpus, solo propone):
      python scripts/depurar_noticias.py classify
    Genera un CSV de revisión (revision_noticias.csv) junto a las noticias,
    con columnas: id, fecha, categoria, decision, confianza, titulo, url, ...
    Tú revisas y, si quieres, editas la columna `decision` a mano.

  Fase 2 — aplicar (materializa el corpus depurado):
      python scripts/depurar_noticias.py apply
    Lee el CSV de revisión y escribe un .txt limpio por cada noticia marcada
    como INCLUIR en la carpeta de salida, listo para `python app.py --ingest`.

Criterios de inclusión (fases pre / durante / post del festival):
  - programación y horarios          (cartel, conciertos, entradas, jornadas)
  - artistas                          (bandas, entrevistas, crónicas de directo)
  - experiencia del visitante         (ambiente, público, imágenes, vivencia)
  - logística práctica                (accesos, transporte, La Fica, normativa)
  - turismo y cultura                 (Murcia, gastronomía, qué ver, impacto)
  - antecedentes e impacto del evento (ediciones, cifras de asistencia, balance)

Criterios de exclusión (ruido para el asistente):
  - política / conflicto institucional (elecciones, partidos, mociones, plenos)
  - contenido ajeno al festival y al destino turístico

Las noticias dudosas (señal política mezclada con festival, meteorología,
quejas, baja confianza) se marcan REVISAR para decisión humana — y son el
conjunto natural sobre el que aplicar más adelante una pasada con el LLM.
"""

import re
import csv
import json
import argparse
import unicodedata
from pathlib import Path

# ─────────────────────────────────────────────
# RUTAS POR DEFECTO
# ─────────────────────────────────────────────

NEWS_DIR    = Path(__file__).resolve().parent.parent / "festival_txts_big" / "festival_txts" / "salida_laverdad_warmup_tema"
INPUT_JSON  = NEWS_DIR / "noticias_warmup_laverdad.json"
REVIEW_CSV  = NEWS_DIR / "revision_noticias.csv"
OUTPUT_DIR  = NEWS_DIR / "noticias_depuradas"

# ─────────────────────────────────────────────
# TAXONOMÍA DE CATEGORÍAS  (criterios transparentes y auditables)
# Cada categoría: lista de patrones (regex con límites de palabra) que la señalan.
# `policy`: INCLUIR (aporta valor) | EXCLUIR (ruido) | REVISAR (ambiguo).
# ─────────────────────────────────────────────

CATEGORIES = {
    "programacion": {
        "policy": "INCLUIR",
        "patterns": [r"cartel", r"line[ -]?up", r"entradas?", r"abonos?", r"horarios?",
                     r"conciertos?", r"jornadas?", r"viernes", r"s[áa]bado", r"programaci[oó]n",
                     r"confirmad", r"actuar[áa]n?", r"sustitu", r"baja del cartel"],
    },
    "artistas": {
        "policy": "INCLUIR",
        "patterns": [r"banda", r"grupo", r"artista", r"cantante", r"dj\b", r"entrevista",
                     r"cr[óo]nica", r"directo", r"gira", r"[áa]lbum", r"disco", r"escenario",
                     r"hechiz", r"enamor", r"telonero"],
    },
    "experiencia": {
        "policy": "INCLUIR",
        "patterns": [r"ambiente", r"im[áa]genes", r"en im[áa]genes", r"p[úu]blico",
                     r"asistentes", r"vivi[óo]", r"as[íi] se vivi", r"galer[íi]a",
                     r"fotos?", r"fan[ae]?s"],
    },
    "logistica": {
        "policy": "INCLUIR",
        "patterns": [r"la fica", r"recinto", r"acceso", r"aparcamiento", r"transporte",
                     r"autob[úu]s", r"parking", r"cashless", r"pulsera", r"normativa",
                     r"seguridad", r"limpieza", r"organizaci[óo]n", r"aforo", r"servicios"],
    },
    "turismo_cultura": {
        "policy": "INCLUIR",
        "patterns": [r"murcia", r"gastronom", r"tapas?", r"restaurante", r"hotel",
                     r"qu[ée] ver", r"turis", r"cultura", r"patrimonio", r"huerta",
                     r"plaza", r"museo"],
    },
    "impacto": {
        "policy": "INCLUIR",
        "patterns": [r"\d[\d.\s]*asistentes", r"r[ée]cord", r"balance", r"edici[oó]n",
                     r"impacto", r"econ[óo]mic", r"recauda", r"llen[óo]", r"hist[óo]ri"],
    },
    "meteo": {
        "policy": "REVISAR",  # relevante pre-festival pero genérico: que lo confirme un humano
        "patterns": [r"lluvia", r"chubascos?", r"previsi[óo]n", r"tiempo\b", r"meteo",
                     r"temperatura", r"inestabilidad", r"aemet"],
    },
    "politica": {
        "policy": "EXCLUIR",
        # OJO: usar \b para evitar falsos positivos (p.ej. \bmoci[óo]n evita
        # que "moción" empareje dentro de "emoción/emociona/emocionante").
        "patterns": [r"\bvox\b", r"abascal", r"\bpsoe\b", r"\bpp\b", r"electoral",
                     r"elecciones", r"\bmoci[óo]n", r"\bpleno\b", r"diputaci[óo]n",
                     r"\bpartido\b", r"\bgobierno\b", r"institucional", r"comicios",
                     r"esca[ñn]os?", r"campa[ñn]a electoral", r"investidura"],
    },
}

# Una coincidencia en el TÍTULO pesa más que en el cuerpo (más informativa).
WEIGHT_TITLE   = 3
WEIGHT_SUMMARY = 2
WEIGHT_TEXT    = 1


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────

def _norm(s: str) -> str:
    """Minúsculas sin acentos, para emparejar patrones de forma robusta."""
    s = (s or "").lower()
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


# Pre-normalizamos los patrones igual que el texto (sin acentos) para que
# `previsi[óo]n` y `previsi[oo]n` casen sobre texto sin tildes.
_COMPILED = {
    cat: [re.compile(_norm(p)) for p in cfg["patterns"]]
    for cat, cfg in CATEGORIES.items()
}


def _slug(title: str, max_len: int = 50) -> str:
    s = _norm(title).replace("| la verdad", "")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s[:max_len] or "noticia"


def classify_record(rec: dict) -> dict:
    """Puntúa una noticia por categoría y devuelve categoría, decisión y confianza."""
    t_title   = _norm(rec.get("title", ""))
    t_summary = _norm(rec.get("summary", ""))
    t_text    = _norm(rec.get("text", ""))

    scores = {}
    pol_topical = 0       # señal política SOLO en titular/sumario (topicalidad real)
    pol_distinct = 0      # nº de términos políticos DISTINTOS (señal de tema institucional)
    for cat, patterns in _COMPILED.items():
        s = 0
        for pat in patterns:
            n_title, n_sum, n_text = len(pat.findall(t_title)), len(pat.findall(t_summary)), len(pat.findall(t_text))
            s += WEIGHT_TITLE * n_title + WEIGHT_SUMMARY * n_sum + WEIGHT_TEXT * n_text
            if cat == "politica":
                pol_topical += WEIGHT_TITLE * n_title + WEIGHT_SUMMARY * n_sum
                if n_title or n_sum or n_text:
                    pol_distinct += 1
        scores[cat] = s

    total = sum(scores.values())
    primary = max(scores, key=scores.get) if total else "sin_categoria"
    confidence = (scores[primary] / total) if total else 0.0
    value_score = sum(v for c, v in scores.items() if CATEGORIES.get(c, {}).get("policy") == "INCLUIR")

    # ── Lógica de decisión ──────────────────────────────────────────────
    # La política solo descarta si es TÓPICA (titular/sumario) o si aparecen
    # varios términos políticos distintos (conflicto institucional). Un único
    # término suelto en el cuerpo no contamina una noticia claramente de valor.
    if primary == "politica":
        decision = "EXCLUIR"             # el tema dominante de la noticia es político
    elif value_score == 0 and (pol_topical > 0 or pol_distinct >= 1):
        decision = "EXCLUIR"              # contenido puramente político
    elif pol_topical > 0 and pol_topical >= value_score:
        decision = "EXCLUIR"             # la política domina el tema
    elif pol_topical > 0 or pol_distinct >= 2:
        decision = "REVISAR"             # política presente pero el festival también
    elif primary == "meteo":
        decision = "REVISAR"             # genérico: relevante pre-festival, lo decide un humano
    elif value_score == 0:
        decision = "REVISAR"             # sin señal de valor ni política → ajeno, revisar
    else:
        decision = "INCLUIR"

    return {
        "categoria": primary,
        "decision": decision,
        "confianza": round(confidence, 2),
        "score_politica": scores.get("politica", 0),
        "score_valor": value_score,
    }


# ─────────────────────────────────────────────
# FASE 1 — CLASIFICAR
# ─────────────────────────────────────────────

def cmd_classify(input_json: Path, review_csv: Path) -> None:
    data = json.loads(input_json.read_text(encoding="utf-8"))
    rows = []
    for i, rec in enumerate(data):
        res = classify_record(rec)
        rows.append({
            "id": i,
            "fecha": (rec.get("date") or "")[:10],
            "categoria": res["categoria"],
            "decision": res["decision"],
            "confianza": res["confianza"],
            "score_valor": res["score_valor"],
            "score_politica": res["score_politica"],
            "titulo": (rec.get("title") or "").replace(" | La Verdad", "").strip(),
            "autor": rec.get("author", ""),
            "url": rec.get("url", ""),
        })

    # Orden de revisión: primero lo dudoso, luego excluido, luego incluido.
    order = {"REVISAR": 0, "EXCLUIR": 1, "INCLUIR": 2}
    rows.sort(key=lambda r: (order[r["decision"]], r["categoria"], -r["confianza"]))

    with open(review_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Resumen por decisión y por categoría.
    from collections import Counter
    by_dec = Counter(r["decision"] for r in rows)
    by_cat = Counter(r["categoria"] for r in rows)
    print(f"Clasificadas {len(rows)} noticias → {review_csv}\n")
    print("Por decisión:")
    for dec in ("INCLUIR", "REVISAR", "EXCLUIR"):
        print(f"  {dec:<8} {by_dec.get(dec, 0)}")
    print("\nPor categoría:")
    for cat, n in by_cat.most_common():
        print(f"  {cat:<16} {n}")
    print(f"\nRevisa la columna `decision` en {review_csv.name} y luego ejecuta:")
    print("  python scripts/depurar_noticias.py apply")


# ─────────────────────────────────────────────
# FASE 2 — APLICAR
# ─────────────────────────────────────────────

def cmd_apply(input_json: Path, review_csv: Path, output_dir: Path) -> None:
    if not review_csv.exists():
        raise SystemExit(f"No existe {review_csv}. Ejecuta primero: classify")

    data = json.loads(input_json.read_text(encoding="utf-8"))
    decisions = {}
    with open(review_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            decisions[int(row["id"])] = (row["decision"].strip().upper(), row["categoria"])

    output_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for i, rec in enumerate(data):
        decision, categoria = decisions.get(i, ("REVISAR", "sin_categoria"))
        if decision != "INCLUIR":
            continue
        title = (rec.get("title") or "").replace(" | La Verdad", "").strip()
        fecha = (rec.get("date") or "")[:10]
        body = (
            f"TÍTULO: {title}\n"
            f"FECHA: {fecha}\n"
            f"AUTOR: {rec.get('author', '')}\n"
            f"FUENTE: {rec.get('url', '')}\n"
            f"CATEGORÍA: {categoria}\n\n"
            f"{(rec.get('text') or '').strip()}\n"
        )
        fname = f"{i:02d}_{categoria}_{_slug(title)}.txt"
        (output_dir / fname).write_text(body, encoding="utf-8")
        written += 1

    print(f"Escritas {written} noticias depuradas en {output_dir}")
    print("\nIMPORTANTE: el bundle original noticias_warmup_laverdad.txt (~277 KB)")
    print("sigue presente y se ingeriría como un único bloque gigante. Antes de")
    print("`--ingest`, mueve/elimina ese .txt para que solo entren las depuradas.")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Depuración semiautomática de noticias para el corpus RAG")
    parser.add_argument("command", choices=["classify", "apply"], help="Fase a ejecutar")
    parser.add_argument("--input", type=Path, default=INPUT_JSON, help="JSON de noticias de entrada")
    parser.add_argument("--review-csv", type=Path, default=REVIEW_CSV, help="CSV de revisión")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR, help="Carpeta de salida (.txt depurados)")
    args = parser.parse_args()

    if args.command == "classify":
        cmd_classify(args.input, args.review_csv)
    else:
        cmd_apply(args.input, args.review_csv, args.output_dir)


if __name__ == "__main__":
    main()
