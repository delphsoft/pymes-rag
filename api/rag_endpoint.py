"""
api/rag_endpoint.py — RAG query API for Pymes Studio
Drop-in endpoint that replaces the generic LLM call in Asesor IA.

Endpoints:
  POST /rag/query    — answer a question with grounded context
  GET  /rag/health   — check index stats
  POST /rag/ingest   — trigger pipeline run (admin only)

Compatible with the existing Next.js / Vercel setup via HTTP.
Run locally: uvicorn api.rag_endpoint:app --port 8001
Or deploy to Railway/Fly.io as a separate microservice.
"""
import os
import json
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException, Header
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from storage.store import load_accepted_chunks, DATA_DIR

app = FastAPI(title="Pymes Studio RAG API", version="1.0.0") if HAS_FASTAPI else None

if app:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://pymesstudio.com", "https://*.vercel.app",
                       "http://localhost:3000"],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )


# ── Simple in-memory index (no Qdrant needed for V1)
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


def simple_search(query: str, top_k: int = 5,
                  segment: str = "universal",
                  jurisdiccion: str = "nacional") -> list[dict]:
    """
    Keyword-based search for V1 (before Qdrant).
    Fast, zero infra, good enough for early users.
    """
    index = get_index()
    query_words = set(query.lower().split())

    scored = []
    for item in index:
        # Score by keyword overlap in preview + topics + questions
        searchable = (
            item.get("preview", "").lower() + " " +
            " ".join(item.get("topics", [])) + " " +
            item.get("source_name", "").lower()
        )
        overlap = sum(1 for w in query_words if w in searchable)
        if overlap > 0:
            # Boost by quality score
            final_score = overlap * item.get("quality_score", 5.0) / 10.0

            # Filter by segment if specified
            if segment != "universal" and item.get("segment") not in (segment, "universal"):
                continue

            scored.append((final_score, item))

    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:top_k]]


def load_full_chunk(chunk_id: str) -> dict | None:
    """Load full chunk content from accepted folder."""
    path = DATA_DIR / "accepted" / f"{chunk_id}.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


# ── API Models
if HAS_FASTAPI:
    class QueryRequest(BaseModel):
        question: str
        segment: Optional[str] = "universal"
        jurisdiccion: Optional[str] = "nacional"
        vertical: Optional[str] = "universal"
        top_k: Optional[int] = 5

    class QueryResponse(BaseModel):
        question: str
        context_chunks: list[dict]
        sources: list[str]
        total_found: int
        ready_for_llm: str  # formatted context string to inject into LLM prompt


    # ── Endpoints
    @app.get("/rag/health")
    async def health():
        index = get_index()
        return {
            "status": "ok",
            "indexed_chunks": len(index),
            "data_dir": str(DATA_DIR),
            "has_data": len(index) > 0,
        }

    @app.post("/rag/query", response_model=QueryResponse)
    async def query_rag(req: QueryRequest):
        results = simple_search(
            query=req.question,
            top_k=req.top_k,
            segment=req.segment,
            jurisdiccion=req.jurisdiccion,
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron chunks relevantes. "
                       "Ejecutá el pipeline primero: python pipeline.py"
            )

        # Load full content for top results
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

        # Build context string for LLM injection
        context_parts = []
        for i, c in enumerate(full_chunks, 1):
            source_label = c["source_name"]
            if c.get("rg_numero"):
                source_label += f" ({c['rg_numero']})"
            if c.get("vigencia_desde"):
                source_label += f" — vigente desde {c['vigencia_desde']}"
            context_parts.append(
                f"[Fuente {i}: {source_label}]\n{c['content']}"
            )

        context_str = "\n\n---\n\n".join(context_parts)

        return QueryResponse(
            question=req.question,
            context_chunks=full_chunks,
            sources=sources,
            total_found=len(full_chunks),
            ready_for_llm=context_str,
        )


# ── Integration example for Pymes Studio Next.js
NEXTJS_EXAMPLE = '''
// app/api/asesor/route.ts — Replace generic LLM call with RAG-grounded call
// Add this BEFORE the Claude/OpenAI call

const RAG_URL = process.env.RAG_API_URL || "http://localhost:8001"

export async function POST(request: Request) {
  const { question, segment, jurisdiccion } = await request.json()

  // 1. Get grounded context from RAG
  const ragRes = await fetch(`${RAG_URL}/rag/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, segment, jurisdiccion, top_k: 5 })
  })

  let groundedContext = ""
  let sources: string[] = []

  if (ragRes.ok) {
    const ragData = await ragRes.json()
    groundedContext = ragData.ready_for_llm
    sources = ragData.sources
  }

  // 2. Inject context into LLM prompt
  const systemPrompt = `Sos un asesor contable y fiscal argentino experto.
Respondé basándote EXCLUSIVAMENTE en la siguiente información oficial y citada.
Si la información no está en el contexto, decí que no tenés datos suficientes
y recomendá consultar con el contador.

CONTEXTO OFICIAL:
${groundedContext}

Reglas:
- Siempre citá la fuente (ej: "Según RG 5329...")
- Si hay montos o fechas, confirmalas con la vigencia
- No inventes datos que no estén en el contexto`

  // 3. Call LLM with grounded context
  const llmResponse = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY!,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      system: systemPrompt,
      messages: [{ role: "user", content: question }]
    })
  })

  const llmData = await llmResponse.json()
  const answer = llmData.content[0].text

  return Response.json({ answer, sources })
}
'''

if __name__ == "__main__":
    print("Next.js integration example:")
    print(NEXTJS_EXAMPLE)
