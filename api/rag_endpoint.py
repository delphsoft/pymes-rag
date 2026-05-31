"""
api/rag_endpoint.py — RAG query API for Pymes Studio
FastAPI service that Railway runs as the web server.
"""
import os
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Pymes Studio RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to pymesstudio.com in prod
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).parent.parent / "data"

_CHUNK_INDEX = None

def get_index():
    global _CHUNK_INDEX
    if _CHUNK_INDEX is None:
        index_path = DATA_DIR / "index" / "accepted_index.json"
        if index_path.exists():
            with open(index_path, encoding="utf-8") as f:
                _CHUNK_INDEX = json.load(f)
        else:
            _CHUNK_INDEX = []
    return _CHUNK_INDEX


def simple_search(query: str, top_k: int = 5, segment: str = "universal") -> list[dict]:
    index = get_index()
    query_words = set(query.lower().split())
    scored = []
    for item in index:
        searchable = (
            item.get("preview", "").lower() + " " +
            " ".join(item.get("topics", [])) + " " +
            item.get("source_name", "").lower()
        )
        overlap = sum(1 for w in query_words if w in searchable)
        if overlap > 0:
            final_score = overlap * item.get("quality_score", 5.0) / 10.0
            if segment != "universal" and item.get("segment") not in (segment, "universal"):
                continue
            scored.append((final_score, item))
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:top_k]]


def load_full_chunk(chunk_id: str) -> dict | None:
    path = DATA_DIR / "accepted" / f"{chunk_id}.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


class QueryRequest(BaseModel):
    question: str
    segment: Optional[str] = "universal"
    jurisdiccion: Optional[str] = "nacional"
    top_k: Optional[int] = 5


class QueryResponse(BaseModel):
    question: str
    context_chunks: list[dict]
    sources: list[str]
    total_found: int
    ready_for_llm: str


@app.get("/")
async def root():
    return {"status": "ok", "service": "Pymes Studio RAG API", "version": "1.0.0"}


@app.get("/rag/health")
async def health():
    index = get_index()
    return {
        "status": "ok",
        "indexed_chunks": len(index),
        "has_data": len(index) > 0,
    }


@app.post("/rag/query", response_model=QueryResponse)
async def query_rag(req: QueryRequest):
    results = simple_search(query=req.question, top_k=req.top_k, segment=req.segment)

    if not results:
        return QueryResponse(
            question=req.question,
            context_chunks=[],
            sources=[],
            total_found=0,
            ready_for_llm="",
        )

    full_chunks = []
    sources = []
    for item in results:
        full = load_full_chunk(item["id"])
        if full:
            full_chunks.append({
                "content": full["content_clean"],
                "source_name": full["source_name"],
                "source_url": full["source_url"],
                "rg_numero": full.get("rg_numero"),
                "vigencia_desde": full.get("vigencia_desde"),
                "quality_score": full["quality_score"],
                "topics": full["topics"],
            })
            if full["source_url"] not in sources:
                sources.append(full["source_url"])

    context_parts = []
    for i, c in enumerate(full_chunks, 1):
        label = c["source_name"]
        if c.get("rg_numero"):
            label += f" ({c['rg_numero']})"
        if c.get("vigencia_desde"):
            label += f" — vigente desde {c['vigencia_desde']}"
        context_parts.append(f"[Fuente {i}: {label}]\n{c['content']}")

    return QueryResponse(
        question=req.question,
        context_chunks=full_chunks,
        sources=sources,
        total_found=len(full_chunks),
        ready_for_llm="\n\n---\n\n".join(context_parts),
    )
