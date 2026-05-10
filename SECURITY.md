# Security

CivicInspect is municipal inspection-support software. Current version: 0.2.0. Do not deploy it as a system of record unless the deployment adds production identity, tenant scoping, audit logging, backup, and operations controls.

When `CIVICINSPECT_CASE_DB_URL` is configured, persisted staff review queue routes require `CIVICINSPECT_STAFF_API_KEY`, `X-CivicInspect-Role: staff` or `service`, and a matching `X-CivicInspect-Staff-Key` from a trusted staff or service workflow. This local API-key gate is a release safeguard, not a replacement for production identity, tenant scoping, and audit logging.

Report suspected vulnerabilities privately to the project maintainer. Do not open public issues containing exploit details, secrets, or sensitive municipal data.
