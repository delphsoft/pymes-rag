"""
crawler/arca.py — ARCA / AFIP data crawler for Pymes Studio RAG
Targets:
  - Tablas de Monotributo (categorías, montos, vencimientos)
  - Resoluciones Generales relevantes
  - Calendario fiscal
  - Constancia condición IVA (via AfipSDK — ya lo tenés integrado)
"""
import httpx
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Generator
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from schema import RagChunk


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PymeStudioBot/1.0; +https://pymesstudio.com/bot)",
    "Accept-Language": "es-AR,es;q=0.9",
}

ARCA_SOURCES = {
    "monotributo_tablas": {
        "url": "https://www.afip.gob.ar/monotributo/categorias.asp",
        "source_name": "ARCA - Categorías Monotributo",
        "topics": ["monotributo", "categorias", "limites_facturacion", "cuota"],
        "segment": "monotributo",
        "rg_ref": "RG 5329",
    },
    "monotributo_inicio": {
        "url": "https://www.afip.gob.ar/monotributo/",
        "source_name": "ARCA - Monotributo inicio",
        "topics": ["monotributo", "inscripcion", "recategorizacion"],
        "segment": "monotributo",
    },
    "iva_responsable": {
        "url": "https://www.afip.gob.ar/iva/",
        "source_name": "ARCA - IVA Responsable Inscripto",
        "topics": ["iva", "responsable_inscripto", "debito_fiscal", "credito_fiscal"],
        "segment": "responsable_inscripto",
    },
    "calendario_fiscal": {
        "url": "https://www.afip.gob.ar/genericos/guiaDePasos/vencimientos.asp",
        "source_name": "ARCA - Calendario Fiscal",
        "topics": ["vencimientos", "calendario", "fechas_pago"],
        "segment": "universal",
    },
    "autonomos": {
        "url": "https://www.afip.gob.ar/autonomos/",
        "source_name": "ARCA - Autónomos",
        "topics": ["autonomos", "aportes", "jubilacion"],
        "segment": "responsable_inscripto",
    },
    "ganancias_pymes": {
        "url": "https://www.afip.gob.ar/ganancias/",
        "source_name": "ARCA - Impuesto a las Ganancias PyMES",
        "topics": ["ganancias", "impuesto", "pyme", "deduccion"],
        "segment": "responsable_inscripto",
    },
}


def fetch_page(url: str, timeout: int = 15) -> str | None:
    try:
        r = httpx.get(url, headers=HEADERS, timeout=timeout, follow_redirects=True)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"  [WARN] fetch failed {url}: {e}")
        return None


def extract_text_blocks(html: str, min_length: int = 80) -> list[str]:
    """Extract meaningful text blocks from HTML, strip nav/footer noise."""
    soup = BeautifulSoup(html, "lxml")

    # Remove noise elements
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "aside", "noscript", "iframe", "form"]):
        tag.decompose()

    blocks = []
    for elem in soup.find_all(["p", "li", "td", "th", "h1", "h2", "h3",
                                "h4", "div", "article", "section"]):
        text = elem.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= min_length and text not in blocks:
            blocks.append(text)

    return blocks


def chunk_blocks(blocks: list[str], max_tokens: int = 400) -> list[str]:
    """
    Group text blocks into chunks of ~max_tokens words.
    Keeps semantic boundaries (doesn't split mid-block).
    """
    chunks = []
    current = []
    current_len = 0

    for block in blocks:
        block_len = len(block.split())
        if current_len + block_len > max_tokens and current:
            chunks.append(" ".join(current))
            current = [block]
            current_len = block_len
        else:
            current.append(block)
            current_len += block_len

    if current:
        chunks.append(" ".join(current))

    return chunks


def crawl_arca_source(key: str, config: dict) -> Generator[RagChunk, None, None]:
    url = config["url"]
    print(f"\n[ARCA] Crawling: {config['source_name']}")

    html = fetch_page(url)
    if not html:
        return

    blocks = extract_text_blocks(html)
    chunks_text = chunk_blocks(blocks)
    total = len(chunks_text)
    print(f"  -> {total} chunks extracted")

    for i, text in enumerate(chunks_text):
        chunk = RagChunk.from_text(
            text=text,
            source_url=url,
            source_type="arca",
            source_name=config["source_name"],
            topics=config.get("topics", []),
            segment=config.get("segment", "universal"),
            vertical="universal",
            jurisdiccion="nacional",
            rg_numero=config.get("rg_ref"),
            vigencia_desde=datetime.utcnow().strftime("%Y-%m-01"),
            chunk_index=i,
            total_chunks=total,
        )
        yield chunk


def crawl_all_arca() -> list[RagChunk]:
    all_chunks = []
    for key, config in ARCA_SOURCES.items():
        for chunk in crawl_arca_source(key, config):
            all_chunks.append(chunk)
    print(f"\n[ARCA] Total chunks: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = crawl_all_arca()
    sample = chunks[0] if chunks else None
    if sample:
        print("\n--- Sample chunk ---")
        print(f"ID: {sample.id}")
        print(f"Source: {sample.source_name}")
        print(f"Topics: {sample.topics}")
        print(f"Content preview: {sample.content_clean[:200]}...")
