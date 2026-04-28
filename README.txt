CivicInspect
============

CivicInspect is the CivicSuite module for inspection support: repeat-case lookup, inspector-owned report drafting, notice draft support, and records-ready inspection exports.

Current state: v0.1.1 inspection support foundation release. It ships deterministic sample helpers, civiccore==0.3.0 alignment, and an accessible public sample UI at /civicinspect.

Not shipped: official findings, citations, fines, notices, inspection scheduling, legal advice, live photo analysis, live LLM calls, or system-of-record integrations.

API surface:
- GET /
- GET /health
- GET /civicinspect
- POST /api/v1/civicinspect/cases/repeat-lookup
- POST /api/v1/civicinspect/reports/draft
- POST /api/v1/civicinspect/notices/draft
- POST /api/v1/civicinspect/export

License: code Apache License 2.0; documentation CC BY 4.0.
