"""
judge/quality_scorer.py — LLM-as-judge for Pymes Studio RAG
Domain-specific rubric for Argentine accounting & tax regulation chunks.
Uses Claude claude-sonnet-4-20250514 via Anthropic API.
"""
import json
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from schema import RagChunk

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


JUDGE_SYSTEM = """Sos un evaluador experto en normativa tributaria y contable argentina.
Tu trabajo es calificar fragmentos de texto que van a alimentar una base de conocimiento
para contadores y dueños de PyMES argentinas.

Respondé SOLO con un objeto JSON válido, sin texto adicional, sin backticks."""

JUDGE_PROMPT = """Evaluá este fragmento de texto en 4 dimensiones, puntaje 1-10 cada una:

1. COMPLETITUD: ¿La idea está completamente expresada? ¿No corta en el medio de algo importante?
   - 10: La información es completa y autocontenida
   - 5: Falta algún dato pero lo principal está
   - 1: Corta antes de dar el dato clave (ej: "el límite es..." sin decir cuánto)

2. PRECISION: ¿Los datos son internamente consistentes? ¿Los montos/fechas tienen sentido?
   - 10: Datos específicos, montos concretos, fechas claras
   - 5: Información general correcta pero sin datos específicos
   - 1: Inconsistencias internas o datos claramente desactualizados

3. VIGENCIA: ¿Esta información probablemente sigue vigente?
   - 10: Menciona año 2025 o 2026, o es un principio permanente
   - 5: No indica fecha, puede ser actual o no
   - 1: Claramente de años anteriores o de un régimen derogado

4. RELEVANCIA: ¿Qué tan útil es para un contador o dueño de PyME argentina?
   - 10: Responde preguntas concretas sobre ARCA, Monotributo, IVA, IIBB, sueldos, etc.
   - 5: Información general sobre el sistema tributario
   - 1: Boilerplate, navegación del sitio, texto genérico sin valor práctico

SEÑALES DE MALA CALIDAD (bajá puntuación fuertemente si aparecen):
- "Ver Anexo", "Ver tabla adjunta", "según lo dispuesto en..." sin decir qué
- Fragmentos de menú de navegación o links
- "Para más información visitá..." sin dar la info
- Montos del año anterior a 2025 sin aclaración
- Texto que dice "actualizado" sin dar la fecha

SEÑALES DE BUENA CALIDAD (subí puntuación):
- Montos específicos en pesos con año de vigencia
- Número de RG o decreto citado (ej: "RG 5329")
- Fechas de vencimiento concretas (ej: "hasta el día 20 del mes siguiente")
- Categorías con sus límites de facturación
- Alícuotas específicas (ej: "21% de IVA", "3% de IIBB en Córdoba")

Fragmento a evaluar:
{chunk_text}

Información adicional:
- Fuente: {source_name}
- Temas detectados: {topics}
- Segmento: {segment}

Respondé EXACTAMENTE con este JSON (sin nada más):
{{
  "completitud": <número 1-10>,
  "precision": <número 1-10>,
  "vigencia": <número 1-10>,
  "relevancia": <número 1-10>,
  "score_total": <promedio con 1 decimal>,
  "razon": "<una oración explicando la calificación principal>",
  "decision": "<accepted|quarantine|rejected>"
}}

Reglas de decisión:
- accepted: score_total >= 6.5
- quarantine: score_total >= 4.0 y < 6.5
- rejected: score_total < 4.0"""


def score_chunk_with_claude(chunk: RagChunk, api_key: str) -> dict:
    """Score a chunk using Claude as judge. Returns quality breakdown."""
    if not HAS_ANTHROPIC:
        return _fallback_score(chunk)

    client = anthropic.Anthropic(api_key=api_key)

    prompt = JUDGE_PROMPT.format(
        chunk_text=chunk.content_clean[:1500],  # cap at 1500 chars
        source_name=chunk.source_name,
        topics=", ".join(chunk.topics) if chunk.topics else "general",
        segment=chunk.segment,
    )

    try:
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            system=JUDGE_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        # Strip any accidental backticks
        raw = re.sub(r"```json|```", "", raw).strip()
        result = json.loads(raw)
        return result
    except Exception as e:
        print(f"  [JUDGE WARN] {e} — using fallback")
        return _fallback_score(chunk)


def _fallback_score(chunk: RagChunk) -> dict:
    """
    Rule-based fallback when API unavailable.
    Good enough for development/testing.
    """
    text = chunk.content_clean.lower()
    score = 5.0

    # Boost signals
    if any(w in text for w in ["rg ", "resolución general", "decreto"]):
        score += 1.0
    if any(w in text for w in ["2025", "2026"]):
        score += 1.0
    if any(c.isdigit() for c in text):  # has numbers = specific data
        score += 0.5
    if any(w in text for w in ["%", "pesos", "$", "límite", "categoría"]):
        score += 0.5

    # Penalty signals
    if any(w in text for w in ["ver anexo", "adjunta", "más información"]):
        score -= 2.0
    if len(chunk.content_clean) < 150:
        score -= 1.5
    if any(w in text for w in ["2022", "2023", "2024"]) and "2025" not in text:
        score -= 1.0

    score = max(1.0, min(10.0, round(score, 1)))

    if score >= 6.5:
        decision = "accepted"
    elif score >= 4.0:
        decision = "quarantine"
    else:
        decision = "rejected"

    return {
        "completitud": score,
        "precision": score,
        "vigencia": score,
        "relevancia": score,
        "score_total": score,
        "razon": "Evaluación automática (fallback rule-based)",
        "decision": decision,
    }


def judge_chunk(chunk: RagChunk, api_key: str | None = None) -> RagChunk:
    """Apply quality scoring to a chunk. Returns updated chunk."""
    key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
    result = score_chunk_with_claude(chunk, key) if key else _fallback_score(chunk)

    chunk.quality_score = result.get("score_total", 0.0)
    chunk.quality_breakdown = {
        "completitud": result.get("completitud", 0),
        "precision": result.get("precision", 0),
        "vigencia": result.get("vigencia", 0),
        "relevancia": result.get("relevancia", 0),
        "razon": result.get("razon", ""),
    }
    chunk.quality_status = result.get("decision", "quarantine")
    return chunk


def judge_batch(chunks: list[RagChunk], api_key: str | None = None,
                verbose: bool = True) -> dict:
    """Judge a list of chunks. Returns stats."""
    accepted = quarantine = rejected = 0

    for i, chunk in enumerate(chunks):
        chunk = judge_chunk(chunk, api_key)
        chunks[i] = chunk  # update in place

        if chunk.quality_status == "accepted":
            accepted += 1
        elif chunk.quality_status == "quarantine":
            quarantine += 1
        else:
            rejected += 1

        if verbose and (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(chunks)}] accepted={accepted} "
                  f"quarantine={quarantine} rejected={rejected}")

    stats = {
        "total": len(chunks),
        "accepted": accepted,
        "quarantine": quarantine,
        "rejected": rejected,
        "acceptance_rate": round(accepted / len(chunks) * 100, 1) if chunks else 0,
    }
    return stats
