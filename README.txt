CivicInspect

CivicInspect is the CivicSuite module for inspection support: repeat-case lookup, inspector-owned report drafting, notice draft support, staff review queues, review-required CivicCode context packets, adversarial local integration mocks, and records-ready inspection exports.

Current state: published v0.2.0 recovery label in active recovery/productization work. This repo provides a FastAPI package aligned to the CivicCore v1.0.0 release wheel, deterministic and database-backed repeat-case lookup, persisted report-draft records, staff-only review queue workflows, review-required inspection context packets, adversarial local integration mocks, notice draft support, records-ready export checklists, and accessible public sample UI at /civicinspect.

Set CIVICINSPECT_CASE_DB_URL to enable persistent repeat-case, report-draft, and staff review records. Persisted staff routes require CIVICINSPECT_STAFF_API_KEY, X-CivicInspect-Role: staff or service, and matching X-CivicInspect-Staff-Key from a trusted staff or service workflow.

CivicInspect does not issue official findings, citations, fines, notices, inspection schedules, legal advice, live photo analysis, live LLM calls, or system-of-record updates.
