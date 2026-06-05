# Audit Lite - Schema Readiness And Import

**Date:** 2026-06-05
**Scope:** CivicInspect local repeat-case import, schema status, and readiness gate.

## Verdict

Pass. CivicInspect now has operator-visible schema status, a validated local repeat-case CSV importer, and readiness endpoints that do not treat sample fallback as customer-ready data.

## Findings

None.

## Behavioral Coverage

- Configured runtime repositories are created with `seed_defaults=False`.
- `/ready` and `/api/v1/civicinspect/readiness` block when `CIVICINSPECT_CASE_DB_URL` is unset.
- Readiness blocks when schema exists but no local repeat-case records have been imported.
- Readiness passes after a local repeat-case record is loaded.
- CSV import validates required columns and row values before writing.
- `civicinspect-db-status` reports schema status and repeat-case count.

## Verification

- `python -m pytest tests/test_production_depth_case_persistence.py tests/test_local_repeat_case_import.py tests/test_runtime_foundation.py -q` - 23 passed.
- `python -m pytest -q` - 35 passed.
