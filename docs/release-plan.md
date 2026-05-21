# CivicInspect Release Plan

## 1 - CivicInspect v1.0.0 Public-Use Module Release

Purpose: inspection assistant for photo/voice-to-report drafting, repeat-case lookup, and notice generation. Inspectors own every decision.

This rung promotes CivicInspect from the current live `v0.2.0` recovery label to current `v1.0.0` release truth only after CivicSuite spec scope, browser UX QA, adversarial validation, docs, tests, release artifacts, source CI, and CivicSuite installer/module-selection truth all pass.

CivicInspect is the active module and can be released only after current spec scope, UX QA, tests, docs, release artifacts, and CivicSuite installer/module-selection truth are proven.

CivicCore remains the shared platform dependency for staff-key-gated review behavior.

Exit criteria:

- CivicInspect package and current-facing docs state `1.0.0`.
- Desktop and mobile browser QA evidence covers the public UI, docs, console, focus, user-visible copy, and relevant rendered states.
- Adversarial integration mocks cover bad inputs, missing or stale records, spoofed or missing staff roles, unavailable dependencies, and permission-boundary failures applicable to the module.
- Local tests, docs verifier, lint/static checks, and release verifier pass.
- GitHub PR merges with green CI.
- GitHub release `v1.0.0` publishes verified wheel, sdist, and SHA256SUMS artifacts.
- CivicSuite suite truth verifies `[civicinspect] PASS 1.0.0` and installer/module-selection evidence on main.
- CivicInspect v1.0.0 source release is verified on main and published with artifacts.
- CivicSuite suite truth verifies CivicInspect 1.0.0 and installer/module-selection evidence on main.
