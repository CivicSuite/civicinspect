CivicInspect
============

CivicInspect is the CivicSuite module for inspection support: repeat-case lookup, inspector-owned report drafting, notice draft support, and records-ready inspection exports.

Current state: published v0.1.1 foundation label under suite-wide release-recovery review. It provides deterministic sample helpers, optional database-backed repeat-case and report-draft records via CIVICINSPECT_CASE_DB_URL, CivicCore v0.3.0 release-wheel alignment, and an accessible public sample UI at /civicinspect. Do not promote it as production software until the recovery gates are complete.

Not shipped: official findings, citations, fines, notices, inspection scheduling, legal advice, live photo analysis, live LLM calls, or system-of-record integrations.

API surface:
- GET /
- GET /health
- GET /civicinspect
- POST /api/v1/civicinspect/cases/repeat-lookup
- POST /api/v1/civicinspect/reports/draft
- GET /api/v1/civicinspect/reports/{report_id} when CIVICINSPECT_CASE_DB_URL is configured
- POST /api/v1/civicinspect/notices/draft
- POST /api/v1/civicinspect/export

Set CIVICINSPECT_CASE_DB_URL to enable persistent repeat-case and report-draft records. When unset, CivicInspect continues to use deterministic in-memory sample data.

License: code Apache License 2.0; documentation CC BY 4.0.
