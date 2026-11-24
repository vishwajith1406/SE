# FinReq AI — Agentic Requirement Intelligence Prototype

A zero-dependency, browser-runnable academic prototype for **Agentic AI-Based Automated Requirement Gathering, Analysis and SDLC Identification System for the Financial Sector**.

## What this project does

FinReq AI helps financial-software teams turn informal stakeholder conversations into reviewable requirements and an explainable SDLC recommendation. It is designed for an academic demonstration, so it runs locally without API keys or cloud services and clearly marks every AI-derived output as advisory.

The system covers digital banking, payments, loans, fraud detection, insurance, investment platforms, KYC, regulatory reporting, and financial analytics scenarios.

## Run

Open `index.html` in a modern browser. For a local web server (recommended), use any static server available on the machine, for example `python -m http.server 8080`, then visit `http://localhost:8080`.

No API key, build tool, or database installation is required. Project state is persisted in browser `localStorage`.

### Two-studio finance portal (reference-style flow)

To run the server-backed version with local signup, isolated studio histories, and downloadable Word documents:

```powershell
python finance_portal.py
```

Open `http://127.0.0.1:8002`. The **Finance SRS Studio** gathers a guided conversation and exports a Finance SRS. The **Finance SDLC Studio** accepts a project statement/SRS evidence, gives a transparent recommendation, and exports its report. These features intentionally use deterministic local demo intelligence because the reference repository's trained QLoRA adapters are not publicly bundled.

## Demonstration flow

1. Open `http://127.0.0.1:8002/platform/`.
2. Choose **Load Demo Project** or create a project profile.
3. Enter informal financial requirements or ingest a local TXT/DOCX file.
4. Select **Analyze Requirements**.
5. Review structured requirements, quality findings, conflicts, and clarification questions.
6. Answer a clarification such as a transfer threshold or response-time target.
7. Review Security & Compliance and Risk Analysis.
8. Open SDLC Recommendation to inspect transparent model scores.
9. Generate and inspect the workflow, traceability matrix, artifacts, and audit trail.
10. Record human approval for the requirement baseline and SDLC recommendation.

## Main features

- 13 logical agents: Coordinator, Stakeholder Interaction, Requirement Extraction, Clarification, Classification, Conflict Detection, Security & Privacy, Compliance, Risk, SDLC Selection, Documentation, Validation, and Human Approval.
- Requirement classification, confidence, source, priority, risk, and review state.
- Ambiguity, incomplete-information, and contradiction detection.
- Local TXT/DOCX ingestion for the platform; local DOCX exports for SRS and SDLC reports.
- Demo security, privacy, compliance, risk, traceability, and audit views.
- Transparent deterministic scoring for Waterfall, V-Model, Agile, Spiral, DevSecOps, and Agile + DevSecOps.
- Project-specific workflow, JSON artifacts, and human approval actions.
- Prompt-injection pattern flagging and low-confidence human-review states.

## Demo

Click **Load Demo Project**, then use Requirements → AI Analysis → Security & Compliance → Risk Analysis → SDLC Recommendation → Workflow. The demo includes clarification questions, structured requirements, controls, risks, scoring, workflow, traceability, artifacts, approval, and audit events.

## Architecture

- **Frontend:** semantic HTML, modern CSS, ES modules.
- **Mock AI provider:** deterministic `DemoAI` extraction and clarification logic in `app.js`, so every demonstration works offline.
- **Agent orchestration:** logical Coordinator, Extraction, Clarification, Classification, Security, Compliance, Risk, SDLC, Documentation, Validation, and Human Approval agent states are exposed in the UI.
- **Knowledge/RAG abstraction:** demo policy references are deliberately labelled as demo sources. Production adapters can add vector retrieval with source, jurisdiction, effective-date, version, and applicability metadata.
- **Persistence:** browser localStorage. A production implementation should move state/audit data to a protected backend database.

The local Python portal (`finance_portal.py`) provides a single launch point for the full platform and the two Word-export studios. It uses the standard library only and binds to `127.0.0.1:8002`.

## SDLC selection

The scoring engine evaluates requirement stability, security criticality, regulatory criticality, and project size. It computes visible suitability scores for Waterfall, V-Model, Agile, Spiral, DevSecOps, and Agile + DevSecOps; it does not randomly ask an LLM to decide. The selected model drives workflow phases.

## Switching to a real LLM

Replace `DemoAI.analyze()` with a backend API client. Keep schema validation for Requirement, Issue, ClarificationQuestion, SecurityFinding, ComplianceMapping, Risk, SDLCScore, WorkflowPhase, and Artifact before persistence. Store provider credentials in server environment variables only (an `.env.example` belongs with that backend); never expose keys in browser code.

## Limitations

This is an academic, client-only prototype. Security controls, RBAC, MFA, encryption, legal/regulatory mappings, document extraction, authentication, server-side audit integrity, and real LLM/RAG are **production implementation required**. Demo compliance mappings are not legal advice or evidence of compliance.

## Repository structure

```text
app.js                 Full browser-based agentic platform
styles.css             Platform UI styles
index.html             Platform entry point
finance_portal.py      Local two-studio portal and local document API
financial_engine.py    Deterministic mock AI and SDLC decision logic
docx_export.py         Dependency-free DOCX generation helper
run_finance_portal.bat Windows launcher
.env.example           Reserved server-side configuration template
```
