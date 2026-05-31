"""
storage/store.py — Storage layer for Pymes Studio RAG
Dev mode: saves to JSON files (no infra needed)
Prod mode: Qdrant vector store + PostgreSQL catalog

Designed to plug into existing Supabase of Pymes Studio via REST API.
"""
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from schema import RagChunk


DATA_DIR = Path(__file__).parent.parent / "data"


def ensure_dirs():
    for d in ["accepted", "quarantine", "rejected", "index"]:
        (DATA_DIR / d).mkdir(parents=True, exist_ok=True)


def save_chunk_json(chunk: RagChunk) -> str:
    """Save chunk to local JSON. Returns filepath."""
    ensure_dirs()
    folder = DATA_DIR / chunk.quality_status
    filepath = folder / f"{chunk.id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chunk.to_dict(), f, ensure_ascii=False, indent=2)
    return str(filepath)


def save_batch(chunks: list[RagChunk], verbose: bool = True) -> dict:
    """Save all chunks sorted by status. Returns summary."""
    ensure_dirs()
    counts = {"accepted": 0, "quarantine": 0, "rejected": 0}

    for chunk in chunks:
        save_chunk_json(chunk)
        counts[chunk.quality_status] = counts.get(chunk.quality_status, 0) + 1

    # Save index file for quick lookup
    index = []
    for chunk in chunks:
        if chunk.quality_status == "accepted":
            index.append({
                "id": chunk.id,
                "source_name": chunk.source_name,
                "topics": chunk.topics,
                "segment": chunk.segment,
                "jurisdiccion": chunk.jurisdiccion,
                "quality_score": chunk.quality_score,
                "vigencia_desde": chunk.vigencia_desde,
                "questions_count": len(chunk.synthetic_questions),
                "preview": chunk.content_clean[:100],
            })

    index_path = DATA_DIR / "index" / "accepted_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    if verbose:
        print(f"\n[STORAGE] Saved: {counts}")
        print(f"[STORAGE] Index: {len(index)} accepted chunks → {index_path}")

    return counts


def load_accepted_chunks() -> list[RagChunk]:
    """Load all accepted chunks from local storage."""
    ensure_dirs()
    chunks = []
    folder = DATA_DIR / "accepted"
    for f in folder.glob("*.json"):
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
            # Reconstruct from dict
            chunk = RagChunk(**data)
            chunks.append(chunk)
    return chunks


def build_qdrant_payload(chunk: RagChunk) -> dict:
    """
    Format chunk for Qdrant upsert.
    Compatible with qdrant-client Python SDK.
    The text to embed = content_clean + synthetic questions joined.
    """
    text_to_embed = chunk.content_clean
    if chunk.synthetic_questions:
        text_to_embed += "\n\nPreguntas relacionadas:\n" + \
                         "\n".join(chunk.synthetic_questions)

    return {
        "id": int(hashlib.md5(chunk.id.encode()).hexdigest()[:8], 16),  # numeric ID
        "payload": {
            "chunk_id": chunk.id,
            "content": chunk.content_clean,
            "source_url": chunk.source_url,
            "source_name": chunk.source_name,
            "source_type": chunk.source_type,
            "topics": chunk.topics,
            "segment": chunk.segment,
            "vertical": chunk.vertical,
            "jurisdiccion": chunk.jurisdiccion,
            "quality_score": chunk.quality_score,
            "vigencia_desde": chunk.vigencia_desde,
            "rg_numero": chunk.rg_numero,
            "synthetic_questions": chunk.synthetic_questions,
            "ingested_at": chunk.ingested_at,
        },
        "text_to_embed": text_to_embed,
    }


def export_for_qdrant(chunks: list[RagChunk]) -> list[dict]:
    """Export accepted chunks formatted for Qdrant batch upsert."""
    return [
        build_qdrant_payload(c)
        for c in chunks
        if c.quality_status == "accepted"
    ]


def print_summary(chunks: list[RagChunk]):
    """Print a readable summary of the pipeline run."""
    total = len(chunks)
    accepted = [c for c in chunks if c.quality_status == "accepted"]
    quarantine = [c for c in chunks if c.quality_status == "quarantine"]
    rejected = [c for c in chunks if c.quality_status == "rejected"]

    print("\n" + "="*50)
    print("PYMES STUDIO RAG — Pipeline Summary")
    print("="*50)
    print(f"Total chunks procesados : {total}")
    print(f"Aceptados               : {len(accepted)} ({len(accepted)/total*100:.0f}%)")
    print(f"En cuarentena           : {len(quarantine)} ({len(quarantine)/total*100:.0f}%)")
    print(f"Rechazados              : {len(rejected)} ({len(rejected)/total*100:.0f}%)")

    if accepted:
        avg_score = sum(c.quality_score for c in accepted) / len(accepted)
        print(f"\nScore promedio (aceptados): {avg_score:.1f}/10")

        topics_count = {}
        for c in accepted:
            for t in c.topics:
                topics_count[t] = topics_count.get(t, 0) + 1
        top_topics = sorted(topics_count.items(), key=lambda x: -x[1])[:5]
        print(f"Top temas: {', '.join(f'{t}({n})' for t, n in top_topics)}")

    print("="*50)
