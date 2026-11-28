# FinReq Studio

FinReq Studio turns a financial system brief and supporting files into one recommended SDLC model and a traceable SRS draft. The interface focuses on those two deliverables. Requirements and retrieved source citations appear inside the SRS document.

## Run on Windows

1. Install Python 3.12 or newer.
2. Copy `.env.example` to `.env` and configure the provider keys below.
3. Double-click `run_finreq.bat`, or run these commands in PowerShell from this folder:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. Keep the server window running while you use the site.

## Provider setup

- **Embeddings are required.** By default, `OPENAI_API_KEY` is used with `text-embedding-3-small`. For a compatible embedding endpoint, set `EMBEDDING_API_KEY`, `EMBEDDING_BASE_URL`, and `EMBEDDING_MODEL`.
- **LLM generation is required.** Set `GROQ_API_KEY`, `OPENAI_API_KEY`, or both. Groq is tried first; OpenAI is the fallback. The same OpenAI key can provide embeddings and generation.
- API keys stay in the server-side `.env` file and are never sent to the browser.

## Retrieval and generation flow

1. The server extracts text from the brief and optional TXT, Markdown, CSV, JSON, PDF, or DOCX files and splits it into overlapping passages.
2. It requests vector embeddings, indexes the passages in a per-analysis ChromaDB collection, and runs semantic searches for the project, functional needs, controls, and integrations.
3. The language model receives retrieved excerpts to draft structured finance requirements and recommend one model from Waterfall, V-Model, Agile, Spiral, DevSecOps, or Agile + DevSecOps. Source citations are restricted to retrieved passage IDs.
4. FinReq assembles a Word SRS locally with requirements, acceptance criteria, assumptions, evidence traceability, the recommendation, and review gates.

## Privacy and review

Briefs and uploaded file text are transmitted to the embedding and LLM providers configured in `.env`. Use synthetic data unless your organization has approved those services for the material. ChromaDB data and downloaded SRS files are stored locally under `data/`; stop the server and remove that folder to clear them. Generated requirements, recommendations, and control statements are drafts. Confirm policy, risk, legal, security, and regulatory decisions with qualified stakeholders.

Uploaded files are limited to 5 MB each, with up to 12 files per analysis. PDF extraction is text-based; scanned image PDFs require OCR and are not supported.
