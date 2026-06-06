import pytest

import civicinspect.main as main_module


@pytest.fixture(autouse=True)
def isolated_civicinspect_runtime_data(monkeypatch, tmp_path):
    monkeypatch.setenv("CIVICINSPECT_DATA_DIR", str(tmp_path / "runtime-data"))
    yield
    main_module._dispose_case_repository()
    main_module._case_db_url = None
