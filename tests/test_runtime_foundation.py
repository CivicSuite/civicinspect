from pathlib import Path
import tomllib

from fastapi.testclient import TestClient

import civicinspect
from civicinspect.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_version_is_100() -> None:
    assert civicinspect.__version__ == "0.2.2"


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicInspect"
    assert payload["version"] == "0.2.2"
    assert payload["status"] == "inspection support product with staff review queues"
    assert "staff review queues" in payload["message"]
    assert "CivicCode context packets" in payload["message"]
    assert "official findings" in payload["message"]
    assert "not implemented" in payload["message"]
    assert "/civicinspect/staff" in payload["next_step"]
    assert "records-ready exports" in payload["next_step"]


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicinspect"
    assert payload["version"] == "0.2.2"
    assert payload["civiccore_version"] == "1.2.0"


def test_release_script_prefers_python3_before_python_for_wsl_native_proof() -> None:
    lines = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8").splitlines()
    python3_line = next(index for index, line in enumerate(lines) if "command -v python3" in line)
    python_line = next(index for index, line in enumerate(lines) if "command -v python >/dev/null" in line)

    assert python3_line < python_line


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = pyproject["project"]["dependencies"]
    assert any(
        dependency
        == "civiccore @ https://github.com/CivicSuite/civiccore/releases/download/v1.2.0/civiccore-1.2.0-py3-none-any.whl#sha256=a94ce958e36fb03c8d961e4db4672ce5bcfa25765c57d75886e999cf15703ec7"
        for dependency in dependencies
    )
    assert pyproject["tool"]["hatch"]["metadata"]["allow-direct-references"] is True


def test_pyproject_exposes_operator_database_scripts() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    scripts = pyproject["project"]["scripts"]
    assert scripts["civicinspect-db-status"] == "civicinspect.db_admin:main"
    assert scripts["civicinspect-import-repeat-cases"] == "civicinspect.data_import:main"


def test_docs_gate_rejects_stale_markers() -> None:
    text = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert '"Shipping v0.1.1"' in text
    assert '"production-ready"' in text
    assert '"official findings are available"' in text


def test_docs_index_marks_v1_label_without_mojibake() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "v0.2.2 inspection support + staff review queues" in text
    assert "staff review queues" in text
    assert "official findings" in text
    assert "Ãƒ" not in text


def test_recovery_status_records_v1_scope() -> None:
    text = (ROOT / "docs" / "release-recovery-status.md").read_text(encoding="utf-8")

    assert "v0.2.2" in text
    assert "staff review queues" in text
