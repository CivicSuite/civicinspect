# CivicInspect

CivicInspect is the CivicSuite module for inspection support: repeat-case lookup, inspector-owned report drafting, notice draft support, and records-ready inspection exports.

Current state: **v0.1.1 inspection support foundation release**. This repo ships a FastAPI package aligned to `civiccore==0.3.0`, health/root endpoints, documentation gates, deterministic sample repeat-case lookup, report draft helper, notice draft helper, records-ready export checklist, and accessible public sample UI at `/civicinspect`. It does **not** ship official findings, citations, fines, notices, inspection scheduling, legal advice, live photo analysis, live LLM calls, or system-of-record integrations.

## What CivicInspect Does

- Looks up deterministic sample repeat-case context for a property.
- Drafts inspection report outlines from inspector-provided notes and photo-observation text.
- Drafts notice text for staff review without issuing any notice.
- Produces records-ready export checklists for inspection case files.
- Demonstrates a public inspection-support UI at `/civicinspect`.

## What CivicInspect Does Not Do

- It does not issue official findings, citations, fines, or notices.
- It does not perform live image recognition or photo analysis.
- It does not schedule inspections or update an inspection system of record.
- It does not provide legal advice.
- It does not call live LLMs in v0.1.1.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and CivicCore versions.
- `GET /civicinspect` returns the accessible public sample UI.
- `POST /api/v1/civicinspect/cases/repeat-lookup` returns sample repeat-case context.
- `POST /api/v1/civicinspect/reports/draft` returns an inspector-review-required report draft.
- `POST /api/v1/civicinspect/notices/draft` returns a notice draft with required staff actions.
- `POST /api/v1/civicinspect/export` returns a records-ready inspection export checklist.

## Local Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code is Apache License 2.0. Documentation is CC BY 4.0.
