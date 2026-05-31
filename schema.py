"""
schema.py — Universal chunk schema for Pymes Studio RAG
Every source, regardless of origin, produces this same structure.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
import hashlib
import json


@dataclass
class RagChunk:
    # Identity
    id: str                          # sha256 of content_raw
    content_raw: str                 # original text, untouched
    content_clean: str               # stripped, normalized

    # Source metadata
    source_url: str
    source_type: str                 # arca | bora | rigi | sas | iibb | manual
    source_name: str                 # "ARCA - Tablas Monotributo 2026"
    published_at: Optional[str]      # ISO date if known
    ingested_at: str                 # ISO datetime, always set
    vigencia_desde: Optional[str]    # when this regulation starts
    vigencia_hasta: Optional[str]    # None = still active

    # Classification
    vertical: str                    # universal | comercio | agro | servicios | construccion
    segment: str                     # monotributo | responsable_inscripto | empleador | pyme
    topics: list                     # ["iva", "monotributo", "categoria_h"]
    jurisdiccion: str                # nacional | bsas | caba | cordoba | ...
    rg_numero: Optional[str]         # "RG 5329" if applicable

    # Quality
    quality_score: float             # 0.0 - 10.0, set by judge
    quality_breakdown: dict          # {completeness, accuracy, freshness, relevance}
    quality_status: str              # accepted | quarantine | rejected

    # Retrieval helpers
    synthetic_questions: list        # LLM-generated questions this chunk answers
    chunk_index: int                 # position within parent document
    total_chunks: int                # total chunks from same document
    parent_doc_id: str               # sha256 of full document

    @classmethod
    def from_text(cls, text: str, source_url: str, source_type: str,
                  source_name: str, **kwargs) -> "RagChunk":
        content_clean = " ".join(text.split())
        chunk_id = hashlib.sha256(text.encode()).hexdigest()[:16]
        parent_id = hashlib.sha256(source_url.encode()).hexdigest()[:16]
        return cls(
            id=chunk_id,
            content_raw=text,
            content_clean=content_clean,
            source_url=source_url,
            source_type=source_type,
            source_name=source_name,
            published_at=kwargs.get("published_at"),
            ingested_at=datetime.utcnow().isoformat(),
            vigencia_desde=kwargs.get("vigencia_desde"),
            vigencia_hasta=kwargs.get("vigencia_hasta"),
            vertical=kwargs.get("vertical", "universal"),
            segment=kwargs.get("segment", "universal"),
            topics=kwargs.get("topics", []),
            jurisdiccion=kwargs.get("jurisdiccion", "nacional"),
            rg_numero=kwargs.get("rg_numero"),
            quality_score=0.0,
            quality_breakdown={},
            quality_status="pending",
            synthetic_questions=[],
            chunk_index=kwargs.get("chunk_index", 0),
            total_chunks=kwargs.get("total_chunks", 1),
            parent_doc_id=parent_id,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
