"""
processor/questions.py — Synthetic question generator for Pymes Studio RAG
For each accepted chunk, generate 3-5 questions a user would ask
whose answer is in that chunk. This dramatically improves retrieval.
"""
import json
import re
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from schema import RagChunk

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


QUESTION_PROMPT = """Dado este fragmento sobre normativa tributaria argentina, generá entre 3 y 5 preguntas concretas que un contador o dueño de PyME podría hacerle a un asistente IA, cuya respuesta está en este texto.

Las preguntas deben:
- Estar en español argentino informal (con "vos")
- Ser específicas, no genéricas
- Representar dudas reales de clientes (no preguntas académicas)
- Incluir variantes de cómo se pregunta lo mismo (técnico y coloquial)

Ejemplos de buenas preguntas:
- "¿Cuánto puedo facturar este año como Monotributista categoría H?"
- "¿Hasta qué fecha tengo para pagar el Monotributo de este mes?"
- "¿Qué pasa si me paso del límite de mi categoría?"

Ejemplos de malas preguntas (demasiado genéricas):
- "¿Qué es el Monotributo?"
- "¿Cómo funciona ARCA?"

Fragmento:
{chunk_text}

Respondé SOLO con un array JSON de strings, sin texto adicional:
["pregunta 1", "pregunta 2", "pregunta 3"]"""


def generate_questions_claude(chunk: RagChunk, api_key: str) -> list[str]:
    if not HAS_ANTHROPIC:
        return _fallback_questions(chunk)

    client = anthropic.Anthropic(api_key=api_key)
    prompt = QUESTION_PROMPT.format(chunk_text=chunk.content_clean[:1200])

    try:
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        questions = json.loads(raw)
        return [q for q in questions if isinstance(q, str) and len(q) > 10]
    except Exception as e:
        print(f"  [Q-GEN WARN] {e}")
        return _fallback_questions(chunk)


def _fallback_questions(chunk: RagChunk) -> list[str]:
    """Rule-based fallback questions based on topics."""
    topic_questions = {
        "monotributo": [
            "¿Cuáles son los límites de facturación de Monotributo?",
            "¿Cuándo vence el pago mensual de Monotributo?",
            "¿Cómo sé si me tengo que recategorizar?",
        ],
        "iva": [
            "¿Cómo calculo el IVA débito fiscal?",
            "¿Qué es el IVA crédito fiscal y cómo lo uso?",
            "¿Cuándo presento la declaración jurada de IVA?",
        ],
        "iibb": [
            "¿Cuánto pago de Ingresos Brutos?",
            "¿Qué alícuota de IIBB corresponde a mi actividad?",
            "¿Cuándo vence IIBB en Córdoba?",
        ],
        "sueldos": [
            "¿Cómo calculo las contribuciones patronales?",
            "¿Qué descuentos tiene un empleado en el recibo de sueldo?",
            "¿Cuándo hay que pagar los sueldos?",
        ],
        "vencimientos": [
            "¿Cuáles son los vencimientos impositivos de este mes?",
            "¿Hasta qué fecha puedo pagar sin recargo?",
        ],
    }

    questions = []
    for topic in chunk.topics:
        if topic in topic_questions:
            questions.extend(topic_questions[topic])
        if len(questions) >= 4:
            break

    return questions[:4] if questions else [
        f"¿Qué dice ARCA sobre {chunk.source_name.lower()}?"
    ]


def add_questions_to_chunk(chunk: RagChunk, api_key: str | None = None) -> RagChunk:
    key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
    if key:
        chunk.synthetic_questions = generate_questions_claude(chunk, key)
    else:
        chunk.synthetic_questions = _fallback_questions(chunk)
    return chunk


def add_questions_batch(chunks: list[RagChunk], api_key: str | None = None,
                        only_accepted: bool = True) -> list[RagChunk]:
    """Add synthetic questions to all accepted chunks."""
    target = [c for c in chunks if not only_accepted or c.quality_status == "accepted"]
    print(f"[Q-GEN] Generating questions for {len(target)} chunks...")

    for i, chunk in enumerate(target):
        chunk = add_questions_to_chunk(chunk, api_key)
        if (i + 1) % 20 == 0:
            print(f"  [{i+1}/{len(target)}] done")

    return chunks
