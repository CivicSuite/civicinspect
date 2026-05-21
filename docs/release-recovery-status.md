# CivicInspect Release-Recovery Status

Date: 2026-05-21

## Status

CivicInspect `v1.0.0` is the active CivicSuite inspection-support release target. This update promotes the demoted `0.2.0` recovery label into current v1 release truth by rechecking staff review queues, review-required CivicCode/case context packets, adversarial local integration mocks, CivicCore v1.1.0 alignment, current-facing documentation, and browser QA evidence.

## Current Runtime Boundary

The package provides deterministic and optional database-backed repeat-case lookup, inspector-owned report draft helpers, persisted report-draft records, staff-only review queues, notice draft helpers, records-ready export checklist support, review-required inspection context packets, adversarial local integration mocks, and a sample public UI at `/civicinspect`.

It does not issue official findings, citations, fines, notices, inspection schedules, legal advice, live photo analysis, live LLM calls, or system-of-record updates.

## Recovery Evidence

- Local `scripts/verify-release.sh` must pass with tests, documentation gate, placeholder import check, Ruff, wheel build, sdist build, and SHA256 generation before the release tag is moved.
- Browser QA covered `/civicinspect` and `docs/index.html` at desktop 1440 x 1000 and mobile 390 x 844.
- Browser QA recorded zero console messages, zero page errors, no horizontal overflow, visible v1.0.0 copy, visible staff review copy, and visible boundary copy.
- Staff review queue tests prove create/list/update/summary and auth rejection behavior.
- Adversarial mock tests prove spoofed roles, attempted findings/citations/fines, stale context, and live photo-analysis claims are blocked for staff review.
- Browser QA summary: `docs/browser-qa-civicinspect-v1.0.0-summary.md`.

## Promotion Rule

CivicInspect may be called v1.0.0 current release truth only after the release gate, browser QA, docs, release-gate audit, PR/CI, GitHub release artifacts, CivicSuite suite-truth PR, and queue evidence are complete.
