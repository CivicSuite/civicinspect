#!/usr/bin/env bash
set -euo pipefail

required=(
  "README.md"
  "README.txt"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "LICENSE-CODE"
  "LICENSE-DOCS"
  ".gitignore"
  "AGENTS.md"
  "USER-MANUAL.md"
  "SECURITY.md"
  "SUPPORT.md"
  "CODE_OF_CONDUCT.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/ISSUE_TEMPLATE/bug_report.md"
  ".github/ISSUE_TEMPLATE/feature_request.md"
  ".github/ISSUE_TEMPLATE/config.yml"
  "docs/RECONCILIATION.md"
  "docs/MILESTONES.md"
  "docs/IMPLEMENTATION_PLAN.md"
  "docs/careful-work-civicinspect-v1.0.0.md"
  "docs/release-gate-audit-civicinspect-v1.0.0.md"
  "docs/browser-qa-civicinspect-v1.0.0-summary.md"
  "docs/github-discussions-seed.md"
  "MILESTONE_0_7_DONE.md"
  "docs/index.html"
  "pyproject.toml"
  "civicinspect/__init__.py"
  "civicinspect/main.py"
  "civicinspect/case_lookup.py"
  "civicinspect/integration_mocks.py"
  "civicinspect/report_draft.py"
  "civicinspect/notice_draft.py"
  "civicinspect/records_export.py"
  "civicinspect/public_ui.py"
)

echo "==> Required-artifact check"
for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "FAIL: missing required artifact: $file" >&2
    exit 1
  fi
done

echo "==> Current-facing shipped/planned truth check"
current_files=("README.md" "README.txt" "USER-MANUAL.md" "docs/index.html")
bad_markers=(
  "Shipping v0.1.1"
  "product-ready"
  "product ready"
  "production-ready"
  "production ready"
  "â"
  "official findings are available"
  "legal advice is available"
  "live GIS is available"
  "live LLM calls are available"
  "inspection scheduling is available"
  "system-of-record integrations are available"
  "production staff-review queues are available"
  "v0.1.1 foundation under recovery review"
)

for file in "${current_files[@]}"; do
  for marker in "${bad_markers[@]}"; do
    if grep -Fqi "$marker" "$file"; then
      echo "FAIL: stale/planned-as-shipped marker '$marker' found in $file" >&2
      exit 1
    fi
  done
done

echo "VERIFY-DOCS: PASSED"
