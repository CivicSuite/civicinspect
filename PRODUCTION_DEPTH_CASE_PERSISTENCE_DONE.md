# Production-Depth Case Persistence Done

Date: 2026-04-28

## Scope

This slice adds optional database-backed repeat-case and report-draft records while preserving deterministic sample behavior when no database URL is configured.

## Shipped

- `CIVICINSPECT_CASE_DB_URL` enables persistent repeat-case and report-draft records.
- `InspectionCaseRepository` stores seeded sample repeat-case records and generated report drafts.
- `POST /api/v1/civicinspect/reports/draft` returns a `report_id` when persistence is configured.
- `GET /api/v1/civicinspect/reports/{report_id}` retrieves persisted report records when persistence is configured.

## Still Not Shipped

- Official findings, citations, fines, or notices.
- Inspection scheduling.
- Legal advice.
- Live photo analysis or live LLM calls.
- System-of-record integrations or writes.

## Verification

- Repository persistence tests must pass.
- API persistence and retrieval tests must pass.
- Full release verification must pass before push/merge.
- Browser QA evidence must confirm `docs/index.html` renders the updated persistence status at desktop and mobile widths with zero console errors.
