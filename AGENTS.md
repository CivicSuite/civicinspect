# CivicInspect Agent Contract

## Source of Truth

- Upstream suite spec: `CivicSuite/civicsuite/docs/CivicSuiteUnifiedSpec.md`, especially the CivicInspect catalog entry and suite-wide non-negotiables.
- CivicInspect supports inspection report drafting, repeat-case lookup, notice draft support, and records-ready exports.
- Inspectors own every decision.

## Hard Boundaries

- CivicInspect never issues official findings, citations, fines, notices, schedules inspections, or updates an inspection system of record.
- CivicInspect never provides legal advice.
- CivicInspect v0.1.0 must not call live LLMs, perform live photo analysis, or rely on production case-system integrations.
- Report and notice drafts must be marked review-required.
- CivicInspect depends on CivicCore; CivicCore must never depend on CivicInspect.
- CivicInspect may reference CivicCode concepts only through released contracts or deterministic sample data in v0.1.0.

## Verification

Run `bash scripts/verify-release.sh` before every push or release.
