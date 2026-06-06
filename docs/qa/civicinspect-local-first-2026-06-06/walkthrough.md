# CivicInspect Local-First Walkthrough

**Date:** 2026-06-06  
**Scope:** CivicInspect public UI, staff UI, readiness, persistence-backed draft creation, and integration contracts after the local-first staff workspace slice.

## Verdict

Passed with one documented runtime limitation in the local walkthrough harness: the server was launched without `CIVICINSPECT_STAFF_API_KEY`, so staff queue loading correctly returned an actionable 503. The suite installer now supplies `CIVICINSPECT_STAFF_API_KEY`, and unit tests cover keyed staff queue success.

## Evidence

- `walkthrough-evidence.json`
- `public-desktop.png`
- `public-mobile.png`
- `staff-desktop.png`
- `staff-mobile.png`

## What Was Exercised

- `GET /civicinspect` on desktop and mobile.
- Public draft workflow through `POST /api/v1/civicinspect/reports/draft`.
- `GET /civicinspect/staff` on desktop and mobile.
- Staff draft workflow through the same persisted report-draft API.
- Staff queue load error path without configured staff key.
- `GET /api/v1/civicinspect/readiness`.
- `GET /api/v1/civicinspect/integration-contracts`.

## Results

- Public page title rendered: `CivicInspect Inspection Support`.
- Public draft flow produced `Draft ready for staff review` with repeat-case context and disclaimer.
- Staff page title rendered: `CivicInspect Staff Workspace`.
- Staff draft flow created persisted report IDs and staff review IDs.
- Readiness returned `ready=true`, `schema_ready=true`, `using_default_local_database=true`, and `repeat_case_count=2`.
- Integration contracts returned:
  - `civicinspect.inspection_report_draft.v1`
  - `civicinspect.staff_review_queue.v1`
  - `civicinspect.records_export_checklist.v1`
- Desktop and mobile viewport checks showed no horizontal overflow.

## Findings

None.

## Watch Item

The staff workspace currently asks for the local staff key and shows the staff queue only when the service is launched with `CIVICINSPECT_STAFF_API_KEY`. That is acceptable for this local-first stage because the suite installer provides the key and the API returns an actionable error when it is missing.
