"""Deterministic demo intelligence for the local Finance Requirements Portal.

Replace these functions with a validated LLM provider in production. The output
is deliberately framed as a draft that needs business, security, and compliance
approval.
"""
from datetime import date

def srs_reply(message: str, history: list[dict]) -> str:
    lower = message.lower()
    if len(history) == 0:
        return ("I will create a finance-domain SRS draft. To establish a safe baseline, "
                "please confirm: (1) user roles, (2) transaction/payment limits, "
                "(3) jurisdictions or internal policies, (4) availability target, and "
                "(5) any integrations or legacy systems.")
    if any(x in lower for x in ("limit", "threshold", "amount")):
        return ("Recorded as a proposed business rule. I will mark its source as stakeholder input "
                "and link it to step-up authentication, audit evidence, and acceptance tests.")
    if any(x in lower for x in ("regulation", "compliance", "rbi", "pci", "policy")):
        return ("Recorded as a compliance input. The final SRS will identify it as supplied evidence "
                "only; human compliance validation remains required before approval.")
    return ("Recorded. I will preserve this as source evidence, convert it to a testable requirement "
            "where possible, and keep unresolved values in the open-issues register.")

def requirements_from_history(history: list[dict]) -> list[tuple[str,str,str,str]]:
    evidence = " ".join(x["content"] for x in history if x["role"] == "user").lower()
    rows = [
        ("FR-FIN-001", "The system shall allow authenticated customers to view available account balances.", "Functional", "High"),
        ("FR-FIN-002", "The system shall allow authorized customers to initiate payments or transfers to eligible beneficiaries.", "Functional / Security", "Critical"),
        ("SEC-FIN-001", "The system shall require step-up authentication for transactions exceeding the human-approved threshold.", "Security", "Critical"),
        ("NFR-AVL-001", "The system shall meet a human-approved availability target and record service interruptions.", "Availability", "High"),
        ("PRV-FIN-001", "The system shall protect personal and financial data using approved access-control and encryption measures.", "Privacy / Security", "Critical"),
        ("AUD-FIN-001", "The system shall create auditable records for sensitive financial actions and approvals.", "Audit / Reporting", "High"),
    ]
    if "loan" in evidence:
        rows.append(("FR-LON-001", "The system shall allow authorized staff to review loan applications against approved decision criteria.", "Functional / Regulatory", "High"))
    if "fraud" in evidence:
        rows.append(("SEC-FRD-001", "The system shall flag potentially anomalous transactions for authorized review.", "Security / Operational", "High"))
    return rows

def srs_sections(project: str, history: list[dict]) -> list[tuple[str,str]]:
    source = "\n".join(f"- {x['content']}" for x in history if x['role'] == 'user') or "- No stakeholder evidence supplied."
    reqs = requirements_from_history(history)
    req_text = "\n".join(f"{rid}: {statement} (Category: {category}; Priority: {priority})" for rid,statement,category,priority in reqs)
    return [
        ("1. Document purpose and control", f"{project} — draft finance software requirements specification. Status: Needs human review. Generated {date.today().isoformat()}."),
        ("2. Problem statement and objectives", "This draft formalizes informal stakeholder statements into reviewable requirements for a financial-sector system. It does not establish legal or regulatory compliance."),
        ("3. Stakeholders and roles", "Business owner, customer or end user, operations team, security team, compliance officer, risk owner, engineering team, and auditor. Role permissions require explicit approval."),
        ("4. Discovery record", source),
        ("5. Functional and non-functional requirements", req_text),
        ("6. Security, privacy, and compliance", "Proposed controls: least privilege, strong authentication, transaction integrity, audit logging, encryption, secure session handling, and evidence-based compliance review. Applicable rules/policies must be supplied and validated by a compliance officer."),
        ("7. Acceptance and verification", "Each requirement requires testable acceptance criteria, negative-case testing, traceability to source evidence, security testing where applicable, and human review before baseline approval."),
        ("8. Risk, assumptions, and open issues", "Open issues: transaction threshold, target availability, applicable jurisdictions/policies, retention duration, and integration constraints. These must be resolved by assigned owners."),
        ("9. Traceability and approval", "Source evidence → requirement ID → design/workflow phase → test case → approval status. This is a draft and has no approval signatures."),
    ]

def choose_sdlc(text: str) -> tuple[str, list[str], list[tuple[str,int]]]:
    lower = text.lower()
    security = any(x in lower for x in ("security", "secure", "fraud", "payment", "bank", "financial", "authentication"))
    changing = any(x in lower for x in ("change", "feedback", "iterat", "evolv", "agile"))
    regulated = any(x in lower for x in ("regulat", "compliance", "audit", "rbi", "policy"))
    scores = {"Waterfall": 48, "V-Model": 58, "Agile": 55, "Spiral": 51, "DevSecOps": 55, "Agile + DevSecOps": 60}
    if security: scores["DevSecOps"] += 23; scores["Agile + DevSecOps"] += 19; scores["V-Model"] += 8
    if changing: scores["Agile"] += 22; scores["Agile + DevSecOps"] += 20; scores["Waterfall"] -= 8
    if regulated: scores["V-Model"] += 18; scores["Agile + DevSecOps"] += 12
    ranked = sorted(((k, min(v, 96)) for k,v in scores.items()), key=lambda x:x[1], reverse=True)
    winner = ranked[0][0]
    reasons = [
        "Financial data and transaction flows require visible security controls and audit evidence." if security else "The supplied evidence does not establish a security profile; confirm it with the security owner.",
        "Requirements are expected to evolve, so iterative stakeholder review is valuable." if changing else "Requirement volatility was not established; validate whether change is expected.",
        "Regulatory or policy checkpoints require documented review and approval." if regulated else "Applicable regulations and policies remain an open question.",
        "The recommendation is a transparent prototype score and requires project-owner approval.",
    ]
    return winner, reasons, ranked

def sdlc_report(project: str, context: str) -> str:
    winner, reasons, ranked = choose_sdlc(context)
    alternatives = "\n".join(f"- {name}: {score}% prototype suitability" for name,score in ranked[1:4])
    return f"""# SDLC Recommendation — {project}

## Recommended approach
**{winner}** — {ranked[0][1]}% prototype suitability.

## Why this approach fits
""" + "\n".join(f"{i+1}. {reason}" for i,reason in enumerate(reasons)) + f"""

## Applied phases
1. Requirements validation and source traceability
2. Backlog or plan approval
3. Architecture and threat modeling
4. Development with peer review
5. Automated functional, security, and integration testing
6. Compliance evidence review and UAT
7. Human approval, deployment, monitoring, and feedback

## Closest alternatives
{alternatives}

## Missing information
- Applicable jurisdiction, regulations, and internal policies
- Maximum transaction threshold and authentication exception process
- Service-level availability and recovery objectives
- Legacy integrations, delivery cadence, and named approval owners

## Review notice
This AI-assisted report is a draft for project, security, and compliance review. It is not legal advice and does not certify compliance.
"""
