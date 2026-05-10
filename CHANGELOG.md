# Changelog

## [0.2.0] - 2026-05-10

- Demoted the false v1.0.0 release label after the external CivicSuite audit found this module is a recovery/foundation module, not a canonical spec-complete v1 product.
- Preserved the useful recovery work while resetting the public package version to 0.2.0.
- Kept the CivicCore v1.0.0 wheel dependency and pinned it with SHA256 for release integrity.
- Supersedes the prior public v1.0.0 posture; do not treat v1.0.0 as production-ready or spec-complete.

All notable changes to CivicInspect will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- feat(deps): bump civiccore pin to v1.0.1 (security hardening recovery patch)

### Added

- CivicInspect v0.2.0 product lane: staff review queues, review-required CivicCode/case context packets, adversarial local integration mocks, and current-facing v1 docs.
- Production-depth case persistence slice with `CIVICINSPECT_CASE_DB_URL`, persisted repeat-case records, persisted report-draft records, and retrieval by `report_id`.
- Suite-wide release-recovery status, WSL-native release-gate proof, browser QA evidence, and regression checks that keep the published v0.1.1 label provisional.

### Changed

- Updated package version and current-facing release gate to `1.0.0`.
- Aligned CivicInspect with the published CivicCore v1.0.0 release wheel.
- Replaced the unresolved `civiccore==0.3.0` package dependency with the published CivicCore v0.3.0 release wheel so fresh installs do not rely on a hidden CI preinstall step.
- Updated release verification to prefer `python3` before `python` so WSL runs use native Linux Python when available.

## [0.1.1] - 2026-04-28

### Changed

- Aligned CivicInspect to `civiccore==0.3.0` while preserving the v0.1 inspection support foundation behavior.
- Updated release gates, CI wheel install, docs, tests, and browser-visible version copy for the v0.1.1 compatibility release.

## [0.1.0] - 2026-04-27

### Added

- FastAPI package/runtime foundation pinned to `civiccore==0.2.0`.
- Repeat-case lookup helper using deterministic sample case data.
- Inspector-owned report draft helper.
- Notice draft helper with required staff-review actions.
- Records-ready inspection export checklist.
- Accessible public sample UI at `/civicinspect` with browser QA coverage.
- Release gate: tests, docs, placeholder import guard, Ruff, and build artifact checks.

### Not Shipped

- Official findings, citations, fines, notices, inspection scheduling, legal advice, live photo analysis, live LLM calls, and system-of-record integrations.
