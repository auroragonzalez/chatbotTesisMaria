"""
Preprocesado de archivos de HORARIOS: convierte las tablas con pipes
(`Día | Escenario | Artista | hora`) en PROSA natural que repite
día + año + festival en cada párrafo, para que cada chunk sea autocontenido
y el retriever (embeddings e5) los encuentre mucho mejor.

- Detecta automáticamente los .txt cuya cabecera contiene `[CATEGORY]: HORARIOS`.
- Soporta el formato de 4 campos (con día por línea) y el de 3 campos (con
  cabecera `[DAY]:`).
- Hace copia de seguridad `<archivo>.orig` (no se ingesta, solo **/*.txt).
- Reescribe el .txt manteniendo el nombre (para no romper evidence_file).

Uso:
    python scripts/preprocess_horarios.py            # aplica
    python scripts/preprocess_horarios.py --dry-run  # solo muestra
"""
import re, sys, shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
CORPUS = ROOT / "festival_txts_big" / "warm_up"

DRY = "--dry-run" in sys.argv


def parse(text: str):
    event = day_hdr = source = apertura = escenarios = None
    rows = []  # (dia, escenario, artista, hora)
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("[EVENT]:"):
            event = s.split(":", 1)[1].strip()
        elif s.startswith("[DAY]:"):
            day_hdr = s.split(":", 1)[1].strip()
        elif s.startswith("[SOURCE_PAGE]:"):
            source = s.split(":", 1)[1].strip()
        elif s.lower().startswith("apertura de puertas"):
            apertura = s.split(":", 1)[1].strip()
        elif s.lower().startswith("escenarios:"):
            escenarios = s.split(":", 1)[1].strip()
        elif " | " in s:
            parts = [p.strip() for p in s.split("|")]
            if len(parts) == 4:
                rows.append(tuple(parts))
            elif len(parts) == 3:
                rows.append((day_hdr, parts[0], parts[1], parts[2]))
    return event, source, apertura, escenarios, rows


def year_of(event: str) -> str:
    m = re.search(r"\b(20\d\d)\b", event or "")
    return m.group(1) if m else ""


def day_phrase(day: str, year: str) -> str:
    d = (day or "").strip()
    if not d:
        return f"de {year}" if year else ""
    # "Viernes 1 de mayo" -> "viernes 1 de mayo de 2026"
    d = d[0].lower() + d[1:]
    if year and year not in d:
        d = f"{d} de {year}"
    return d


def fmt_time(t: str) -> str:
    t = t.strip()
    if "-" in t:
        ini, fin = [x.strip() for x in t.split("-", 1)]
        return f"de {ini} a {fin}"
    return f"a las {t}"


def to_prose(path: Path) -> str:
    event, source, apertura, escenarios, rows = parse(path.read_text(encoding="utf-8"))
    year = year_of(event)
    out = [f"{event} — Horarios oficiales del festival (cartel por día y hora, con artistas y horas de actuación)."]
    out.append("Recinto: La Fica (Murcia)." + (f" Fuente oficial: {source}." if source else ""))
    if apertura:
        out.append(f"Apertura de puertas del {event}: {apertura}.")
    if escenarios:
        out.append(f"Escenarios del {event}: {escenarios}.")

    # Agrupa por día (orden de aparición) y, dentro, por escenario (orden de aparición)
    days = []
    by_day = {}
    for dia, esc, art, hora in rows:
        if dia not in by_day:
            by_day[dia] = {}
            days.append(dia)
        by_day[dia].setdefault(esc, []).append((art, hora))

    for dia in days:
        dp = day_phrase(dia, year)
        all_artists = [art for esc in by_day[dia] for art, _ in by_day[dia][esc]]
        out.append("")
        out.append(f"=== Cartel del {dp} ===")
        out.append(
            f"El {dp}, en el {event} (recinto La Fica, Murcia), actúan estos artistas "
            f"por escenario y hora. Cartel completo del {dp}: " + "; ".join(all_artists) + "."
        )
        for esc, acts in by_day[dia].items():
            frag = "; ".join(f"{art} actúa {fmt_time(hora)}" for art, hora in acts)
            out.append(
                f"Escenario {esc}, {dp}, en el {event}: {frag}."
            )
    return "\n".join(out) + "\n"


def main():
    targets = []
    for p in CORPUS.rglob("*.txt"):
        try:
            head = p.read_text(encoding="utf-8")[:200]
        except Exception:
            continue
        if "[CATEGORY]: HORARIOS" in head:
            targets.append(p)

    print(f"Archivos de horarios detectados: {len(targets)}")
    for p in sorted(targets):
        prose = to_prose(p)
        print(f"\n===== {p.relative_to(ROOT)} =====")
        print(prose[:600] + ("..." if len(prose) > 600 else ""))
        if not DRY:
            bak = p.with_suffix(p.suffix + ".orig")
            if not bak.exists():
                shutil.copy2(p, bak)
            p.write_text(prose, encoding="utf-8")
    print(f"\n{'(dry-run, no se escribió nada)' if DRY else 'Reescritos en prosa (backups .orig creados).'}")


if __name__ == "__main__":
    main()
