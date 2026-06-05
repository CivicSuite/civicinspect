from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from civicinspect.case_lookup import DISCLAIMER
from civicinspect.persistence import InspectionCaseRepository


REPEAT_CASE_COLUMNS = {
    "property_key",
    "property_reference",
    "violation_type",
    "related_case_ids",
    "staff_note",
}


@dataclass(frozen=True)
class ImportSummary:
    repeat_cases: int = 0


def import_local_repeat_cases(*, db_url: str, repeat_cases_csv: Path) -> ImportSummary:
    """Validate and import local municipal repeat-case CSV rows into CivicInspect."""

    records = [
        {
            "property_key": _required(row, "property_key"),
            "property_reference": _required(row, "property_reference"),
            "violation_type": _required(row, "violation_type"),
            "related_case_ids": _related_case_ids(row, repeat_cases_csv, index),
            "staff_note": _required(row, "staff_note"),
            "disclaimer": DISCLAIMER,
        }
        for index, row in _read_rows(repeat_cases_csv)
    ]

    repository = InspectionCaseRepository(db_url=db_url, seed_defaults=False)
    try:
        for record in records:
            repository.upsert_repeat_case(**record)
    finally:
        repository.engine.dispose()
    return ImportSummary(repeat_cases=len(records))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Import local municipal repeat-case CSV rows into CivicInspect."
    )
    parser.add_argument(
        "--db-url",
        required=True,
        help="SQLAlchemy database URL for CivicInspect case records.",
    )
    parser.add_argument(
        "--repeat-cases-csv",
        required=True,
        type=Path,
        help="CSV with local repeat-case rows.",
    )
    args = parser.parse_args(argv)

    summary = import_local_repeat_cases(
        db_url=args.db_url,
        repeat_cases_csv=args.repeat_cases_csv,
    )
    print(f"CivicInspect import complete: {summary.repeat_cases} repeat cases.")
    return 0


def _read_rows(path: Path) -> list[tuple[int, dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(REPEAT_CASE_COLUMNS - fieldnames)
        if missing:
            raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
        rows = list(reader)
    for index, row in enumerate(rows, start=2):
        for column in REPEAT_CASE_COLUMNS:
            if row.get(column, "").strip() == "":
                raise ValueError(f"{path}:{index} has an empty required value for {column}")
        _related_case_ids(row, path, index)
    return list(enumerate(rows, start=2))


def _required(row: dict[str, str], column: str) -> str:
    return row[column].strip()


def _related_case_ids(row: dict[str, str], path: Path, index: int) -> tuple[str, ...]:
    case_ids = tuple(case_id.strip() for case_id in row["related_case_ids"].split(";") if case_id.strip())
    if not case_ids:
        raise ValueError(f"{path}:{index} has an empty required value for related_case_ids")
    return case_ids


if __name__ == "__main__":
    raise SystemExit(main())
