# Changelog

All notable changes to CivicInspect will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
