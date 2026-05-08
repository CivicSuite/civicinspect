# CivicInspect Release-Recovery Status

Date: 2026-05-07

## Status

CivicInspect `0.1.1` is a published foundation label under suite-wide release-recovery review. It is not product-ready and must not be promoted as production municipal inspection software.

## Current Runtime Boundary

The current package provides deterministic sample repeat-case lookup, inspector-owned report draft helpers, notice draft helpers, records-ready export checklist support, optional local case/report persistence with `CIVICINSPECT_CASE_DB_URL`, and a sample public UI at `/civicinspect`.

It does not issue official findings, citations, fines, notices, inspection schedules, legal advice, live photo analysis, live LLM calls, or system-of-record updates.

## Recovery Evidence

- WSL-native release verification passed through `scripts/verify-release.sh`: `18 passed`, docs gate passed, placeholder import check passed, Ruff passed, and build artifacts/checksums were created.
- Fresh install proof resolved CivicCore from the published v0.3.0 release wheel without a hidden CI preinstall: `CivicCore: 0.3.0`, `CivicInspect: 0.1.1`, `WSL platform: linux`.
- Browser QA covered `docs/index.html` at desktop 1440 x 1000 and mobile 390 x 844 with console, overflow, and keyboard-focus checks.
- Documentation gates reject stale product-ready language, the old shipping badge, and browser mojibake.

## Promotion Rule

Do not call CivicInspect finished, shippable, production-ready, or product-ready until a later active-module sprint implements the full CivicInspect v1.0.0 definition of done and passes the release gate.
