# Changelog

All notable changes to CivicInspect will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Production-depth case persistence slice with `CIVICINSPECT_CASE_DB_URL`, persisted repeat-case records, persisted report-draft records, and retrieval by `report_id`.

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
