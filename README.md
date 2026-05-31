# Pymes Studio — RAG Data Stack

Sistema de ingesta, curación y consulta de normativa tributaria argentina
para alimentar el **Asesor IA** de Pymes Studio con datos grounded y citados.

## Arquitectura

```
ARCA + BORA + RIGI + manuales
         ↓
    crawler/*.py          ← fetchea y extrae texto
         ↓
    judge/quality_scorer  ← Claude evalúa cada chunk (1-10)
         ↓
    processor/questions   ← genera preguntas sintéticas
         ↓
    storage/store.py      ← guarda en /data/ (JSON dev → Qdrant prod)
         ↓
    api/rag_endpoint.py   ← FastAPI que consume Next.js de Pymes Studio
```

## Setup

```bash
# 1. Clonar / crear carpeta
cd pymes-rag

# 2. Instalar dependencias
pip install requests beautifulsoup4 lxml httpx python-dotenv openai qdrant-client tiktoken fastapi uvicorn anthropic

# 3. Variables de entorno (opcional para V1)
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Uso

### Correr el pipeline completo
```bash
# Sin API key — usa judge fallback (rule-based)
python pipeline.py

# Con Claude como judge (mejor calidad)
python pipeline.py --api-key sk-ant-...

# Solo ARCA
python pipeline.py --source arca

# Solo ver qué crawlea sin guardar
python pipeline.py --dry-run
```

### Iniciar el API server
```bash
pip install fastapi uvicorn
uvicorn api.rag_endpoint:app --port 8001 --reload
```

### Consultar manualmente
```bash
curl -X POST http://localhost:8001/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuánto puedo facturar como Monotributista?", "segment": "monotributo"}'
```

## Estructura de archivos

```
pymes-rag/
├── schema.py                 # Universal chunk schema
├── pipeline.py               # Pipeline orchestrator
├── crawler/
│   ├── arca.py              # ARCA / AFIP crawler
│   └── bora.py              # BORA crawler
├── judge/
│   └── quality_scorer.py    # LLM-as-judge con rubric argentino
├── processor/
│   └── questions.py         # Generador de preguntas sintéticas
├── storage/
│   └── store.py             # JSON dev / Qdrant prod
├── api/
│   └── rag_endpoint.py      # FastAPI + Next.js integration
└── data/
    ├── accepted/            # Chunks calificados ≥ 6.5
    ├── quarantine/          # Chunks 4.0-6.4 (revisar manualmente)
    ├── rejected/            # Chunks < 4.0
    └── index/               # Índice rápido para búsqueda
```

## Agregar nuevas fuentes

```python
# En crawler/arca.py, agregar al dict ARCA_SOURCES:
"nueva_fuente": {
    "url": "https://www.afip.gob.ar/...",
    "source_name": "ARCA - Nombre descriptivo",
    "topics": ["tema1", "tema2"],
    "segment": "monotributo",  # o "responsable_inscripto", "empleador", "universal"
}
```

## Conectar a Pymes Studio (Next.js)

Ver `api/rag_endpoint.py` al final del archivo — tiene el código completo
para reemplazar el llamado genérico al LLM en `app/api/asesor/route.ts`.

Variables de entorno a agregar en Vercel:
```
RAG_API_URL=https://tu-rag-service.railway.app
```

## Verticales y segmentos (para afinar después)

| Segmento | Fuentes prioritarias |
|---|---|
| `monotributo` | ARCA tablas, calendario, RG 5329 |
| `responsable_inscripto` | ARCA IVA, ganancias, autónomos |
| `empleador` | ARCA sueldos, SICOSS, contribuciones |
| `pyme` | RIGI, SAS, PIMI, FOGAR, BCRA líneas |
| `agro` | SENASA, IIBB agropecuario, retenciones |

La columna `vertical` en el schema permite filtrar por industria
cuando el número de clientes por sector lo justifique.

## Roadmap

- [x] Crawlers ARCA + BORA
- [x] LLM judge con rubric argentino
- [x] Preguntas sintéticas
- [x] Storage JSON + índice
- [x] FastAPI endpoint
- [x] Integración Next.js
- [ ] Qdrant vector store (cuando superemos 5k chunks)
- [ ] Neo4j para grafo de relaciones entre RGs
- [ ] Crawler IIBB por provincia (ARBA, AGIP, AGIP Córdoba)
- [ ] Crawler RIGI / SAS / PIMI
- [ ] Cron job nocturno (GitHub Actions o Railway cron)
- [ ] Dashboard de calidad de chunks
