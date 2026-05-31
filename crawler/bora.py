"""
crawler/bora.py — BORA (Boletín Oficial) crawler for Pymes Studio RAG
Targets normativa relevante para PyMES: impuestos, laboral, comercial.
"""
import httpx
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Generator
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from schema import RagChunk


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PymeStudioBot/1.0)",
    "Accept-Language": "es-AR,es;q=0.9",
}

# BORA secciones relevantes para PyMES
BORA_SECTIONS = {
    "primera": "https://www.boletinoficial.gob.ar/secciones/primera",   # leyes, decretos
    "segunda": "https://www.boletinoficial.gob.ar/secciones/segunda",   # RGs ARCA/AFIP
}

# Keywords que indican relevancia para el RAG de PyMES
RELEVANT_KEYWORDS = [
    "monotributo", "monotributista", "responsable inscripto",
    "iva", "ganancias", "ingresos brutos", "iibb",
    "pyme", "mipyme", "micro", "pequeña empresa",
    "autónomo", "empleador", "contribución patronal",
    "resolución general", "régimen simplificado",
    "factura electrónica", "cae", "arca", "afip",
    "rigi", "ley 27742", "economía del conocimiento",
    "sueldo", "liquidación", "blanqueo", "moratoria",
]


def is_relevant(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in RELEVANT_KEYWORDS)


def extract_rg_number(text: str) -> str | None:
    match = re.search(r"Resolución\s+General\s+[Nn]?[°ºo]?\s*(\d+)", text)
    if match:
        return f"RG {match.group(1)}"
    match = re.search(r"RG\s+[Nn]?[°ºo]?\s*(\d+)", text)
    if match:
        return f"RG {match.group(1)}"
    return None


def extract_vigencia(text: str) -> str | None:
    match = re.search(r"(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})", text)
    if match:
        months = {
            "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
            "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
            "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
        }
        d, m_str, y = match.group(1), match.group(2).lower(), match.group(3)
        m = months.get(m_str, "01")
        return f"{y}-{m}-{d.zfill(2)}"
    return None


def fetch_page(url: str) -> str | None:
    try:
        r = httpx.get(url, headers=HEADERS, timeout=20, follow_redirects=True)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"  [WARN] fetch failed {url}: {e}")
        return None


def crawl_bora_section(section_name: str, url: str,
                       days_back: int = 7) -> Generator[RagChunk, None, None]:
    """
    Crawl BORA section, filter relevant normativa, yield chunks.
    days_back: how many days of bulletins to check
    """
    print(f"\n[BORA] Crawling sección {section_name}: {url}")
    html = fetch_page(url)
    if not html:
        return

    soup = BeautifulSoup(html, "lxml")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Extract article-like containers
    items = soup.find_all(["article", "div", "section"], limit=100)
    relevant_texts = []

    for item in items:
        text = item.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 100 and is_relevant(text):
            relevant_texts.append(text)

    # Also grab raw paragraphs
    for p in soup.find_all(["p", "li"]):
        text = p.get_text(strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 100 and is_relevant(text) and text not in relevant_texts:
            relevant_texts.append(text)

    print(f"  -> {len(relevant_texts)} bloques relevantes encontrados")

    for i, text in enumerate(relevant_texts):
        rg = extract_rg_number(text)
        vigencia = extract_vigencia(text)

        # Classify topic
        topics = []
        text_lower = text.lower()
        if "monotributo" in text_lower or "régimen simplificado" in text_lower:
            topics.append("monotributo")
        if "iva" in text_lower:
            topics.append("iva")
        if "ganancias" in text_lower:
            topics.append("ganancias")
        if "ingresos brutos" in text_lower or "iibb" in text_lower:
            topics.append("iibb")
        if "sueldo" in text_lower or "patronal" in text_lower:
            topics.append("sueldos")
        if "pyme" in text_lower or "mipyme" in text_lower:
            topics.append("pyme")
        if "rigi" in text_lower:
            topics.append("rigi")
        if not topics:
            topics.append("normativa_general")

        chunk = RagChunk.from_text(
            text=text,
            source_url=url,
            source_type="bora",
            source_name=f"BORA - Sección {section_name.capitalize()}",
            topics=topics,
            segment="universal",
            vertical="universal",
            jurisdiccion="nacional",
            rg_numero=rg,
            vigencia_desde=vigencia,
            chunk_index=i,
            total_chunks=len(relevant_texts),
        )
        yield chunk


def crawl_all_bora() -> list[RagChunk]:
    all_chunks = []
    for section_name, url in BORA_SECTIONS.items():
        for chunk in crawl_bora_section(section_name, url):
            all_chunks.append(chunk)
    print(f"\n[BORA] Total chunks: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = crawl_all_bora()
    if chunks:
        print(f"\nSample chunk topics: {chunks[0].topics}")
        print(f"Sample RG: {chunks[0].rg_numero}")
        print(f"Preview: {chunks[0].content_clean[:200]}")
