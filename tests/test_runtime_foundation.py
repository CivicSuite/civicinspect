from pathlib import Path
import re
import tomllib

from fastapi.testclient import TestClient

import civicinspect
from civicinspect.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_version_is_011() -> None:
    assert civicinspect.__version__ == "0.1.1"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicInspect"
    assert payload["version"] == "0.1.1"
    assert payload["status"] == "inspection support foundation plus case persistence"
    assert "database-backed repeat-case and report-draft records" in payload["message"]
    assert "official findings" in payload["message"]
    assert "not implemented yet" in payload["message"]
    assert payload["next_step"].startswith("Post-v0.1.1 roadmap")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicinspect"
    assert payload["version"] == "0.1.1"
    assert re.fullmatch(r"\d+\.\d+\.\d+", payload["civiccore_version"])


def test_release_script_prefers_python3_before_python_for_wsl_native_proof() -> None:
    lines = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8").splitlines()
    python3_line = next(index for index, line in enumerate(lines) if "command -v python3" in line)
    python_line = next(
        index
        for index, line in enumerate(lines)
        if "command -v python >/dev/null" in line
    )

    assert python3_line < python_line


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = pyproject["project"]["dependencies"]
    assert any(
        dependency
        == "civiccore @ https://github.com/CivicSuite/civiccore/releases/download/v0.3.0/civiccore-0.3.0-py3-none-any.whl"
        for dependency in dependencies
    )
    assert pyproject["tool"]["hatch"]["metadata"]["allow-direct-references"] is True


def test_docs_gate_rejects_stale_product_ready_and_mojibake_markers() -> None:
    text = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert '"Shipping v0.1.1"' in text
    assert '"product-ready"' in text
    assert '"production-ready"' in text
    assert '"â"' in text


def test_docs_index_marks_foundation_label_provisional_without_mojibake() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "published foundation label under suite-wide release-recovery review" in text
    assert "v0.1.1 foundation under recovery review" in text
    assert "release-recovery-status.md" in text
    assert "â" not in text


def test_recovery_status_blocks_product_promotion() -> None:
    text = (ROOT / "docs" / "release-recovery-status.md").read_text(encoding="utf-8")

    assert "not product-ready" in text
    assert "must not be promoted as production municipal inspection software" in text
