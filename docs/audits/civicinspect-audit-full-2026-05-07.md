# CivicInspect Audit-Full Packet

Date: 2026-05-07
Repo: `CivicSuite/civicinspect`
Mode: release-recovery gate
Local commit audited before fixes: `93f70d4b5e0d1944af863a03bf269422dae13fc8`

## 1. Executive Audit

Static audit confidence: High for release-script, docs, dependency, and test surfaces inspected locally.
Runtime sign-off confidence: High for this release-recovery scope after WSL release verification and browser QA passed.

CivicInspect does not currently overclaim a v1.0.0 product release, but it had release-recovery gaps that weaken trust: fresh installs depended on an implicit CivicCore preinstall, WSL verification could pick Windows Python before Linux Python, and browser docs contained a mojibake title plus an overly promotional shipping badge.

## 2. Audit Coverage Ledger

| Area | Status | Evidence |
|---|---|---|
| Engineering | Checked | `pyproject.toml`, `.github/workflows/verify.yml`, `civicinspect/main.py`, tests |
| Security and authorization | Checked | No secrets found in inspected release surfaces; app remains sample/local boundary |
| UI/UX | Checked | Static docs inspected; Playwright desktop/mobile browser QA passed |
| Product/PM | Checked | README/manual/docs now state provisional foundation label |
| Documentation | Checked | README, text docs, manual, changelog, docs index, recovery status |
| Install/bootstrap/seeding | Checked | Dependency changed to published CivicCore v0.3.0 wheel for fresh installs |
| Version/release consistency | Checked | Version remains `0.1.1`; no v1 promotion |
| Test engineering | Checked | Regression tests added for release verifier, docs gates, direct dependency, and mojibake |
| Runtime QA | Checked | WSL release gate passed; browser QA passed |
| Cross-cutting synthesis | Checked | Main issue class is release-label trust, not feature functionality |

## 3. Claim Verification Matrix

| Claim | Result | Evidence |
|---|---|---|
| CivicInspect is not product-ready | Verified | README/manual/recovery status |
| Version remains `0.1.1` | Verified | `pyproject.toml`, `civicinspect/__init__.py`, tests |
| CivicCore remains dependency-only | Verified static | `civicinspect/main.py` imports CivicCore version only; no reverse dependency in this repo |
| Fresh install can resolve CivicCore | Verified | WSL temp venv installed `civiccore-0.3.0` and `civicinspect-0.1.1` |
| Browser docs are readable | Verified | Playwright desktop/mobile QA passed with no console/page errors |

## 4. What The Dev Team Needs To Do Now

1. Push the recovery branch.
2. Open a PR.
3. Confirm GitHub CI runs the release gate without a hidden CivicCore preinstall.
4. Merge only after CI is green.

## 5. Next-Sprint Watchlist

- Full CivicInspect v1.0.0 scope remains a future active-module sprint, not part of this recovery patch.
- Any future product-ready claim must require Playwright user-flow tests, runtime install proof, consistency gates, docs-source enforcement, and security scans.

## 6. Engineering Deep Dive

Finding ENG-001
Severity: Critical
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: A fresh installer should not need an undocumented CI preinstall step.
Evidence: `pyproject.toml` used `civiccore==0.3.0` while CI separately installed the CivicCore wheel first.
Blast radius: New developer installs, WSL release gates, CI trust.
Fix: Use the published CivicCore v0.3.0 release wheel directly and allow Hatch direct references.

## 7. Security And Authorization Deep Dive

No secret-bearing release surfaces were found in the inspected docs/scripts/tests. CivicInspect still states it does not provide official findings, legal advice, live LLM calls, or system-of-record integrations.

## 8. UI/UX Deep Dive

Finding UX-001
Severity: Major
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: Mojibake in first-viewport docs lowers trust in the project.
Evidence: `docs/index.html` title contained mojibake.
Blast radius: Public docs impression and browser QA credibility.
Fix: Replace with ASCII title and add browser QA proof.

## 9. Product/PM Deep Dive

Finding PM-001
Severity: Major
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: The suite-wide recovery effort requires visible mock-vs-production labeling and provisional status.
Evidence: `docs/index.html` used a "Shipping v0.1.1" badge without recovery caveat.
Blast radius: Public trust and release-status interpretation.
Fix: Mark `0.1.1` as a foundation label under recovery review.

## 10. Documentation Deep Dive

Docs now distinguish current sample/foundation behavior from unshipped production behavior. The docs gate rejects product-ready phrasing, the old shipping badge, and mojibake.

## 11. Install / Bootstrap / Seeding Deep Dive

Finding BOOT-001
Severity: Critical
Confidence: High
Evidence type: Static
Status: Durable defect
Why it matters: CI preinstall masked whether the package itself is installable.
Evidence: Workflow installed CivicCore before installing CivicInspect.
Blast radius: Release trust, new-user onboarding.
Fix: Remove the workflow preinstall and let the package dependency resolve the published wheel.

## 12. Version And Release Consistency Deep Dive

Version remains `0.1.1`. This recovery patch does not promote CivicInspect to v1.0.0.

## 13. Test Engineering Deep Dive

Regression tests cover Python launcher ordering, direct CivicCore wheel dependency, docs gate markers, recovery status copy, and browser-doc encoding.

## 14. Runtime QA Deep Dive

WSL fresh install resolved CivicCore from the published v0.3.0 wheel and imported `civicinspect==0.1.1` on Linux. WSL `scripts/verify-release.sh` passed with `18 passed`, docs gate passed, placeholder import check passed, Ruff passed, and build artifacts/checksums created. Playwright Chromium verified the recovery docs at desktop and mobile widths with no console errors, page errors, mojibake, stale shipping badge, or horizontal overflow; keyboard focus reached the recovery evidence link.

## 15. Cross-Cutting Synthesis

The main defect class was not implementation overreach; it was release-evidence trust. The fix removes hidden install assumptions and makes provisional status visible.

## 16. Verification Gaps And Sign-Off Limits

This packet does not certify CivicInspect as product-ready. It certifies only that the current published foundation label is truthfully represented and locally verifiable for the release-recovery scope.
