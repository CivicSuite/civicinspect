from pathlib import Path

import pytest

from civicinspect.data_import import import_local_repeat_cases, main
from civicinspect.persistence import InspectionCaseRepository


def test_import_local_repeat_cases_loads_valid_csv(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'repeat-cases.db'}"
    csv_path = _write_csv(
        tmp_path,
        "property_key,property_reference,violation_type,related_case_ids,staff_note\n"
        "100 main,100 Main Street,nuisance,case-1;case-2,Confirm local history.\n",
    )

    summary = import_local_repeat_cases(db_url=db_url, repeat_cases_csv=csv_path)

    repository = InspectionCaseRepository(db_url=db_url, seed_defaults=False)
    try:
        result = repository.lookup_repeat_cases(
            property_reference="100 Main Street",
            violation_type="nuisance",
        )
        count = repository.repeat_case_record_count()
    finally:
        repository.engine.dispose()

    assert summary.repeat_cases == 1
    assert count == 1
    assert result.related_case_ids == ("case-1", "case-2")
    assert result.staff_note == "Confirm local history."


def test_import_local_repeat_cases_validates_before_writing(tmp_path) -> None:
    db_url = f"sqlite:///{tmp_path / 'invalid-repeat-cases.db'}"
    csv_path = _write_csv(
        tmp_path,
        "property_key,property_reference,violation_type,related_case_ids,staff_note\n"
        "local main,100 Main Street,nuisance,,Confirm local history.\n",
    )

    with pytest.raises(ValueError, match="related_case_ids"):
        import_local_repeat_cases(db_url=db_url, repeat_cases_csv=csv_path)

    repository = InspectionCaseRepository(db_url=db_url, seed_defaults=False)
    try:
        assert repository.repeat_case_record_count() == 0
    finally:
        repository.engine.dispose()


def test_import_cli_reports_loaded_repeat_cases(tmp_path, capsys) -> None:
    db_url = f"sqlite:///{tmp_path / 'cli-repeat-cases.db'}"
    csv_path = _write_csv(
        tmp_path,
        "property_key,property_reference,violation_type,related_case_ids,staff_note\n"
        "local oak,42 Oak Avenue,building,case-3,Confirm local history.\n",
    )

    exit_code = main(["--db-url", db_url, "--repeat-cases-csv", str(csv_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "CivicInspect import complete: 1 repeat cases." in captured.out


def _write_csv(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "repeat-cases.csv"
    path.write_text(text, encoding="utf-8")
    return path
