from fastapi.testclient import TestClient

import civicinspect.main as main_module
from civicinspect.main import app
from civicinspect.persistence import InspectionCaseRepository


client = TestClient(app)


def test_case_and_report_records_persist(tmp_path) -> None:
    db_path = tmp_path / "case-records.db"
    repository = InspectionCaseRepository(db_url=f"sqlite:///{db_path}")

    repeat = repository.lookup_repeat_cases(property_reference="100 Main Street", violation_type="nuisance")
    stored = repository.create_report(
        inspection_id="insp-100",
        property_reference="100 Main Street",
        inspector_notes="Overgrown vegetation observed.",
        photo_observations=("Photo shows rear alley condition.",),
        voice_notes="Follow-up needed.",
    )
    repository.engine.dispose()

    second_repository = InspectionCaseRepository(db_url=f"sqlite:///{db_path}", seed_defaults=False)
    try:
        reloaded_repeat = second_repository.lookup_repeat_cases(property_reference="100 Main Street")
        reloaded_report = second_repository.get_report(stored.report_id)
    finally:
        second_repository.engine.dispose()

    assert reloaded_repeat.related_case_ids == repeat.related_case_ids
    assert reloaded_report is not None
    assert reloaded_report.inspection_id == "insp-100"
    assert reloaded_report.inspector_review_required is True
    db_path.unlink()


def test_api_uses_configured_case_database(monkeypatch, tmp_path) -> None:
    db_path = tmp_path / "api-case-records.db"
    monkeypatch.setenv("CIVICINSPECT_CASE_DB_URL", f"sqlite:///{db_path}")

    try:
        repeat_response = client.post(
            "/api/v1/civicinspect/cases/repeat-lookup",
            json={"property_reference": "100 Main Street", "violation_type": "nuisance"},
        )
        create_response = client.post(
            "/api/v1/civicinspect/reports/draft",
            json={
                "inspection_id": "insp-100",
                "property_reference": "100 Main Street",
                "inspector_notes": "Overgrown vegetation observed.",
                "photo_observations": ["Photo shows rear alley condition."],
                "voice_notes": "Follow-up needed.",
            },
        )
        report_id = create_response.json()["report_id"]
        get_response = client.get(f"/api/v1/civicinspect/reports/{report_id}")
    finally:
        main_module._dispose_case_repository()
        main_module._case_db_url = None

    assert repeat_response.status_code == 200
    assert repeat_response.json()["repeat_case_count"] == 2
    assert create_response.status_code == 200
    assert report_id
    assert get_response.status_code == 200
    assert get_response.json()["report_id"] == report_id
    db_path.unlink()


def test_report_lookup_requires_configured_database() -> None:
    response = client.get("/api/v1/civicinspect/reports/not-configured")

    assert response.status_code == 503
    assert "Set CIVICINSPECT_CASE_DB_URL" in response.json()["detail"]["fix"]
