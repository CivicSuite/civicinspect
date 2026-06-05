# Audit Lite - CivicCore 1.2.0 Alignment

**Date:** 2026-06-05
**Scope:** CivicInspect CivicCore dependency alignment slice.

## Verdict

Pass. The slice updates CivicInspect's current runtime dependency to the published CivicCore 1.2.0 wheel and makes the dependency contract mutation-visible in tests.

## Findings

None.

## Behavioral Coverage

- `tests/test_runtime_foundation.py` asserts `/health` reports `civiccore_version` as `1.2.0`.
- `tests/test_runtime_foundation.py` asserts `pyproject.toml` uses the exact CivicCore 1.2.0 release wheel URL and SHA256.
- Current-facing docs describe CivicCore 1.2.0 instead of the earlier 1.1.0 alignment.

## Verification

- `python -m pytest tests/test_runtime_foundation.py -q` - 8 passed.
- `python -m pytest -q` - 24 passed.
- `bash scripts/verify-release.sh` - PASSED.
