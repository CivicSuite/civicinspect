from __future__ import annotations

import argparse

from civicinspect.persistence import InspectionCaseRepository


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check and initialize the local CivicInspect case database schema."
    )
    parser.add_argument(
        "--db-url",
        required=True,
        help="SQLAlchemy database URL used by CIVICINSPECT_CASE_DB_URL.",
    )
    args = parser.parse_args()

    repository = InspectionCaseRepository(db_url=args.db_url, seed_defaults=False)
    try:
        status = repository.schema_status()
        repeat_cases = repository.repeat_case_record_count()
    finally:
        repository.engine.dispose()

    ready = "ready" if status.ready else "not ready"
    missing = ", ".join(status.missing_tables) if status.missing_tables else "none"
    version = status.schema_version or "none"
    print(
        "CivicInspect schema "
        f"{ready}: version={version}; expected={status.expected_schema_version}; "
        f"dialect={status.dialect}; missing_tables={missing}; repeat_cases={repeat_cases}."
    )


if __name__ == "__main__":
    main()
