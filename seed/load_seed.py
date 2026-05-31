"""
seed/load_seed.py — Carga el seed manual al data pool de Pymes Studio
Convierte SEED_CHUNKS en RagChunk objects y los guarda en /data/accepted/

Uso:
  cd pymes-rag
  python seed/load_seed.py
  python seed/load_seed.py --with-questions   (agrega preguntas sintéticas extra via Claude)
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from seed.seed_data import SEED_CHUNKS
from schema import RagChunk
from storage.store import save_batch, print_summary, DATA_DIR
import json
from pathlib import Path


def build_chunk_from_seed(raw: dict) -> RagChunk:
    chunk = RagChunk.from_text(
        text=raw["content"],
        source_url=raw["source_url"],
        source_type=raw.get("source_type", "manual"),
        source_name=raw["source_name"],
        topics=raw.get("topics", []),
        segment=raw.get("segment", "universal"),
        vertical=raw.get("vertical", "universal"),
        jurisdiccion=raw.get("jurisdiccion", "nacional"),
        rg_numero=raw.get("rg_numero"),
        vigencia_desde=raw.get("vigencia_desde"),
    )
    # Override ID with stable human-readable key
    chunk.id = raw["id"]
    chunk.quality_score = raw.get("quality_score", 9.0)
    chunk.quality_breakdown = {
        "completitud": raw.get("quality_score", 9.0),
        "precision": raw.get("quality_score", 9.0),
        "vigencia": raw.get("quality_score", 9.0),
        "relevancia": raw.get("quality_score", 9.0),
        "razon": "Seed manual — validado por experto contador",
    }
    chunk.quality_status = "accepted"
    chunk.synthetic_questions = raw.get("synthetic_questions", [])
    chunk.chunk_index = 0
    chunk.total_chunks = 1
    return chunk


def load_seed(with_questions: bool = False, api_key: str | None = None):
    print(f"\n{'='*50}")
    print("Pymes Studio RAG — Cargando seed manual")
    print(f"Total chunks a cargar: {len(SEED_CHUNKS)}")
    print(f"{'='*50}\n")

    chunks = []
    for raw in SEED_CHUNKS:
        chunk = build_chunk_from_seed(raw)
        chunks.append(chunk)
        print(f"  ✓ {chunk.id} — {chunk.source_name[:50]}")

    # Optionally enrich questions via Claude
    if with_questions and api_key:
        print(f"\n[Q-GEN] Enriqueciendo preguntas sintéticas con Claude...")
        from processor.questions import add_questions_batch
        chunks = add_questions_batch(chunks, api_key=api_key, only_accepted=True)

    # Save to storage
    print(f"\n[STORAGE] Guardando {len(chunks)} chunks...")
    save_batch(chunks, verbose=True)

    print_summary(chunks)

    # Show sample questions
    print("\n── Muestra de preguntas sintéticas indexadas ──")
    for chunk in chunks[:3]:
        print(f"\n{chunk.source_name}:")
        for q in chunk.synthetic_questions[:2]:
            print(f"  · {q}")

    print(f"\n✅ Seed cargado. El Asesor IA ya tiene {len(chunks)} chunks de conocimiento.")
    print(f"   Próximo paso: reiniciar el FastAPI server en Railway para que use los nuevos datos.")
    return chunks


def verify_seed():
    """Verify seed loaded correctly by testing a few searches."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from api.rag_endpoint import simple_search, get_index

    # Reset index cache
    import api.rag_endpoint as ep
    ep._CHUNK_INDEX = None

    index = get_index()
    print(f"\n[VERIFY] Chunks en índice: {len(index)}")

    test_queries = [
        "límites facturación Monotributo categoría H",
        "cuándo conviene pasarme a Responsable Inscripto",
        "cuánto pago de cargas sociales por un empleado",
        "IVA crédito fiscal compras",
        "SAS cuándo conviene",
    ]

    print("\n[VERIFY] Pruebas de búsqueda:")
    for q in test_queries:
        results = simple_search(q, top_k=2)
        if results:
            print(f"  ✓ '{q[:45]}...' → {results[0]['source_name'][:40]}")
        else:
            print(f"  ✗ '{q[:45]}...' → SIN RESULTADO")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-questions", action="store_true",
                        help="Enriquecer preguntas via Claude API")
    parser.add_argument("--api-key", default=os.getenv("ANTHROPIC_API_KEY"))
    parser.add_argument("--verify", action="store_true",
                        help="Solo verificar el seed existente")
    args = parser.parse_args()

    if args.verify:
        verify_seed()
    else:
        chunks = load_seed(with_questions=args.with_questions, api_key=args.api_key)
        verify_seed()
