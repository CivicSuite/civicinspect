from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicinspect.case_lookup import SAMPLE_CASES, RepeatCaseResult, lookup_repeat_cases
from civicinspect.report_draft import draft_inspection_report


metadata = sa.MetaData()

repeat_case_records = sa.Table(
    "repeat_case_records",
    metadata,
    sa.Column("property_key", sa.String(255), primary_key=True),
    sa.Column("property_reference", sa.String(500), nullable=False),
    sa.Column("violation_type", sa.String(255), nullable=False),
    sa.Column("related_case_ids", sa.JSON(), nullable=False),
    sa.Column("staff_note", sa.Text(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicinspect",
)

inspection_report_records = sa.Table(
    "inspection_report_records",
    metadata,
    sa.Column("report_id", sa.String(36), primary_key=True),
    sa.Column("inspection_id", sa.String(160), nullable=False),
    sa.Column("property_reference", sa.String(500), nullable=False),
    sa.Column("summary", sa.Text(), nullable=False),
    sa.Column("observation_bullets", sa.JSON(), nullable=False),
    sa.Column("inspector_review_required", sa.Boolean(), nullable=False),
    sa.Column("disclaimer", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicinspect",
)


@dataclass(frozen=True)
class StoredInspectionReport:
    report_id: str
    inspection_id: str
    property_reference: str
    summary: str
    observation_bullets: tuple[str, ...]
    inspector_review_required: bool
    disclaimer: str
    created_at: datetime


class InspectionCaseRepository:
    """SQLAlchemy-backed repeat-case and report-draft records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None, seed_defaults: bool = True) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicinspect": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicinspect"))
        metadata.create_all(self.engine)
        if seed_defaults:
            self.seed_repeat_cases(SAMPLE_CASES.items())

    def seed_repeat_cases(self, cases: Iterable[tuple[str, tuple[str, ...]]]) -> None:
        now = datetime.now(UTC)
        with self.engine.begin() as connection:
            for property_key, case_ids in cases:
                exists = connection.execute(
                    sa.select(repeat_case_records.c.property_key).where(
                        repeat_case_records.c.property_key == property_key.casefold()
                    )
                ).first()
                if exists is not None:
                    continue
                sample = lookup_repeat_cases(property_reference=property_key, violation_type="general inspection")
                connection.execute(
                    repeat_case_records.insert().values(
                        property_key=property_key.casefold(),
                        property_reference=property_key,
                        violation_type=sample.violation_type,
                        related_case_ids=list(case_ids),
                        staff_note=sample.staff_note,
                        disclaimer=sample.disclaimer,
                        created_at=now,
                        updated_at=now,
                    )
                )

    def lookup_repeat_cases(self, *, property_reference: str, violation_type: str = "") -> RepeatCaseResult:
        normalized = property_reference.strip().casefold()
        with self.engine.begin() as connection:
            rows = connection.execute(sa.select(repeat_case_records)).mappings().all()
        for row in rows:
            if row["property_key"] in normalized:
                return RepeatCaseResult(
                    property_reference=property_reference.strip() or row["property_reference"],
                    violation_type=violation_type.strip() or row["violation_type"],
                    repeat_case_count=len(row["related_case_ids"]),
                    related_case_ids=tuple(row["related_case_ids"]),
                    staff_note=row["staff_note"],
                    disclaimer=row["disclaimer"],
                )
        return lookup_repeat_cases(property_reference=property_reference, violation_type=violation_type)

    def create_report(
        self,
        *,
        inspection_id: str,
        property_reference: str,
        inspector_notes: str,
        photo_observations: tuple[str, ...] = (),
        voice_notes: str = "",
    ) -> StoredInspectionReport:
        draft = draft_inspection_report(
            inspection_id=inspection_id,
            property_reference=property_reference,
            inspector_notes=inspector_notes,
            photo_observations=photo_observations,
            voice_notes=voice_notes,
        )
        stored = StoredInspectionReport(
            report_id=str(uuid4()),
            inspection_id=draft.inspection_id,
            property_reference=draft.property_reference,
            summary=draft.summary,
            observation_bullets=draft.observation_bullets,
            inspector_review_required=draft.inspector_review_required,
            disclaimer=draft.disclaimer,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                inspection_report_records.insert().values(
                    report_id=stored.report_id,
                    inspection_id=stored.inspection_id,
                    property_reference=stored.property_reference,
                    summary=stored.summary,
                    observation_bullets=list(stored.observation_bullets),
                    inspector_review_required=stored.inspector_review_required,
                    disclaimer=stored.disclaimer,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_report(self, report_id: str) -> StoredInspectionReport | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(inspection_report_records).where(inspection_report_records.c.report_id == report_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_report(row)


def _row_to_report(row: object) -> StoredInspectionReport:
    data = dict(row)
    return StoredInspectionReport(
        report_id=data["report_id"],
        inspection_id=data["inspection_id"],
        property_reference=data["property_reference"],
        summary=data["summary"],
        observation_bullets=tuple(data["observation_bullets"]),
        inspector_review_required=data["inspector_review_required"],
        disclaimer=data["disclaimer"],
        created_at=data["created_at"],
    )
