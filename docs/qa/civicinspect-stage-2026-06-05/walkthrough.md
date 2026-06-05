# CivicInspect Stage Walkthrough

## Executive Summary

The `/civicinspect` interface is wired to the report-draft API and works in desktop and mobile Chromium checks. The page renders a real draft form, submits to `/api/v1/civicinspect/reports/draft`, displays returned observations, and keeps the no-official-action boundary visible. No interface wiring findings remain.

## Methodology

- Reviewed README, user manual, route definitions, public UI source, persistence code, importer code, readiness code, and tests.
- Launched `civicinspect.main:app` locally on `127.0.0.1:18168`.
- Used Playwright Chromium at 1440x1000 and 390x844.
- Captured screenshots and network/console evidence.
- Exercised `/`, `/health`, `/ready`, `/api/v1/civicinspect/readiness`, valid report draft, and invalid report draft.

## Project Gestalt

CivicInspect is a local-first inspection support module. Its public UI exposes advisory report drafting; API and persistence paths support optional local repeat-case records, report records, and staff review queues; readiness gates prevent sample fallback from being treated as customer-ready local data.

## Findings By Severity

None.

## Missing Or Partial Features

No missing UI wiring was found within the current CivicInspect stage scope. The broader suite still needs installer-level clean-machine validation outside this module stage.

## Backend Or System Capabilities Not Surfaced

The public UI surfaces advisory report drafting. Repeat-case CSV import, schema status, readiness, persisted reports, and staff queues are documented operator/staff surfaces rather than public controls, which matches the module boundary.

## Confusing Or Misleading UI

None found. The UI states that CivicInspect does not issue findings, citations, fines, notices, inspection schedules, or system-of-record updates.

## Broken Or Suspicious Wiring Map

| UI element or workflow | Expected system connection | Actual connection | Status | Evidence |
| --- | --- | --- | --- | --- |
| Draft form | POST report draft API | `fetch("/api/v1/civicinspect/reports/draft")` | Pass | Draft summary rendered |
| Loading/success status | Human-readable state update | `#result` updates during and after fetch | Pass | Playwright captured final result text |
| Invalid report API | 422 actionable validation | Missing `inspector_notes` returned 422 with `fields: ["inspector_notes"]` | Pass | `walkthrough-evidence.json` |
| Mobile layout | No horizontal overflow | `document.documentElement.scrollWidth <= window.innerWidth` | Pass | desktop/mobile evidence |

## Test Assessment

The current tests prove the public UI is API-wired, returned content is rendered without unsafe HTML injection, report API validation is actionable, schema status works, local repeat-case import validates before writing, configured runtime does not seed samples, and readiness flips only after local repeat-case records are loaded. The stage walkthrough adds runtime browser evidence on top of the unit/API suite.

## Recommended Repair Plan

No immediate repairs required for CivicInspect stage scope.

## Confidence And Gaps

High confidence for the local CivicInspect module gate. This walkthrough does not claim suite-level bare-metal installer readiness or cross-module end-to-end packaging readiness.

## Appendix

- Screenshot: `docs/qa/civicinspect-stage-2026-06-05/public-desktop.png`
- Screenshot: `docs/qa/civicinspect-stage-2026-06-05/public-mobile.png`
- Evidence JSON: `docs/qa/civicinspect-stage-2026-06-05/walkthrough-evidence.json`
- `python -m pytest -q` - 36 passed.
- `bash scripts/verify-release.sh` - PASSED.
