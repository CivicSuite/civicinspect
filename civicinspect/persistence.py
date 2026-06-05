from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicinspect.case_lookup import SAMPLE_CASES, RepeatCaseResult, lookup_repeat_cases
from civicinspect.report_draft import draft_inspection_report


metadata = sa.MetaData()
SCHEMA_VERSION = "2026-06-05-001"

schema_migrations = sa.Table(
    "schema_migrations",
    metadata,
    sa.Column("schema_version", sa.String(80), primary_key=True),
    sa.Column("applied_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicinspect",
)

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

staff_review_queue_records = sa.Table(
    "staff_review_queue_records",
    metadata,
    sa.Column("review_id", sa.String(36), primary_key=True),
    sa.Column("report_id", sa.String(36), nullable=True),
    sa.Column("inspection_id", sa.String(160), nullable=False),
    sa.Column("property_reference", sa.String(500), nullable=False),
    sa.Column("status", sa.String(80), nullable=False),
    sa.Column("reason", sa.Text(), nullable=False),
    sa.Column("assigned_to", sa.String(255), nullable=True),
    sa.Column("resolution", sa.Text(), nullable=True),
    sa.Column("created_by", sa.String(255), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    schema="civicinspect",
)


OPEN_STAFF_REVIEW_STATUSES = {"open", "in_review"}
RESOLVED_STAFF_REVIEW_STATUSES = {"resolved", "closed"}
STAFF_REVIEW_STATUSES = OPEN_STAFF_REVIEW_STATUSES | RESOLVED_STAFF_REVIEW_STATUSES


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


@dataclass(frozen=True)
class StaffReviewQueueItem:
    review_id: str
    report_id: str | None
    inspection_id: str
    property_reference: str
    status: str
    reason: str
    assigned_to: str | None
    resolution: str | None
    created_by: str
    created_at: datetime
    updated_at: datetime
    visibility: str = "staff_only"


@dataclass(frozen=True)
class StaffReviewSummary:
    total_items: int
    by_status: dict[str, int]
    open_items: int
    generated_at: datetime
    visibility: str = "staff_only"


@dataclass(frozen=True)
class SchemaStatus:
    schema_version: str | None
    expected_schema_version: str
    ready: bool
    missing_tables: tuple[str, ...]
    dialect: str


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
        self.migrate()
        if seed_defaults:
            self.seed_repeat_cases(SAMPLE_CASES.items())

    def migrate(self) -> SchemaStatus:
        """Apply non-destructive local schema setup and return the resulting status."""

        metadata.create_all(self.engine)
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(schema_migrations.c.schema_version).where(
                    schema_migrations.c.schema_version == SCHEMA_VERSION
                )
            ).first()
            if exists is None:
                connection.execute(
                    schema_migrations.insert().values(
                        schema_version=SCHEMA_VERSION,
                        applied_at=datetime.now(UTC),
                    )
                )
        return self.schema_status()

    def schema_status(self) -> SchemaStatus:
        inspector = sa.inspect(self.engine)
        translated_schema = None if self.engine.dialect.name == "sqlite" else "civicinspect"
        available_tables = set(inspector.get_table_names(schema=translated_schema))
        expected_tables = {
            "repeat_case_records",
            "inspection_report_records",
            "staff_review_queue_records",
            "schema_migrations",
        }
        missing_tables = tuple(sorted(expected_tables - available_tables))
        schema_version = None
        if "schema_migrations" not in missing_tables:
            with self.engine.begin() as connection:
                schema_version = connection.execute(
                    sa.select(schema_migrations.c.schema_version)
                    .order_by(schema_migrations.c.applied_at.desc())
                    .limit(1)
                ).scalar_one_or_none()
        return SchemaStatus(
            schema_version=schema_version,
            expected_schema_version=SCHEMA_VERSION,
            ready=schema_version == SCHEMA_VERSION and not missing_tables,
            missing_tables=missing_tables,
            dialect=self.engine.dialect.name,
        )

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

    def upsert_repeat_case(
        self,
        *,
        property_key: str,
        property_reference: str,
        violation_type: str,
        related_case_ids: tuple[str, ...],
        staff_note: str,
        disclaimer: str,
    ) -> None:
        normalized_key = property_key.strip().casefold()
        if normalized_key == "":
            raise ValueError("property_key is required.")
        if not related_case_ids:
            raise ValueError("related_case_ids must include at least one case id.")
        now = datetime.now(UTC)
        values = {
            "property_reference": property_reference.strip() or property_key.strip(),
            "violation_type": violation_type.strip() or "general inspection",
            "related_case_ids": list(related_case_ids),
            "staff_note": staff_note.strip(),
            "disclaimer": disclaimer.strip(),
            "updated_at": now,
        }
        if values["staff_note"] == "":
            raise ValueError("staff_note is required.")
        if values["disclaimer"] == "":
            raise ValueError("disclaimer is required.")
        with self.engine.begin() as connection:
            exists = connection.execute(
                sa.select(repeat_case_records.c.property_key).where(
                    repeat_case_records.c.property_key == normalized_key
                )
            ).first()
            if exists is None:
                connection.execute(
                    repeat_case_records.insert().values(
                        property_key=normalized_key,
                        created_at=now,
                        **values,
                    )
                )
            else:
                connection.execute(
                    repeat_case_records.update()
                    .where(repeat_case_records.c.property_key == normalized_key)
                    .values(**values)
                )

    def repeat_case_record_count(self) -> int:
        with self.engine.begin() as connection:
            return connection.execute(sa.select(sa.func.count()).select_from(repeat_case_records)).scalar_one()

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

    def create_staff_review_queue_item(
        self,
        *,
        inspection_id: str,
        property_reference: str,
        reason: str,
        created_by: str,
        report_id: str | None = None,
    ) -> StaffReviewQueueItem:
        now = datetime.now(UTC)
        item = StaffReviewQueueItem(
            review_id=str(uuid4()),
            report_id=report_id,
            inspection_id=inspection_id.strip() or "unassigned-inspection",
            property_reference=property_reference.strip() or "unknown property",
            status="open",
            reason=reason,
            assigned_to=None,
            resolution=None,
            created_by=created_by,
            created_at=now,
            updated_at=now,
        )
        with self.engine.begin() as connection:
            connection.execute(staff_review_queue_records.insert().values(**_staff_queue_values(item)))
        return item

    def list_staff_review_queue_items(
        self, *, status: str | None = None
    ) -> tuple[StaffReviewQueueItem, ...]:
        with self.engine.begin() as connection:
            statement = sa.select(staff_review_queue_records).order_by(
                staff_review_queue_records.c.created_at
            )
            if status is not None:
                statement = statement.where(staff_review_queue_records.c.status == status)
            rows = connection.execute(statement).mappings()
        return tuple(_row_to_staff_queue_item(row) for row in rows)

    def update_staff_review_queue_item(
        self,
        *,
        review_id: str,
        status: str,
        assigned_to: str | None,
        resolution: str | None,
    ) -> StaffReviewQueueItem | None:
        if status not in STAFF_REVIEW_STATUSES:
            raise ValueError("status must be one of: closed, in_review, open, resolved.")
        if status in RESOLVED_STAFF_REVIEW_STATUSES and not resolution:
            raise ValueError("resolution is required when resolving or closing a staff review item.")
        current = self.get_staff_review_queue_item(review_id)
        if current is None:
            return None
        updated = StaffReviewQueueItem(
            review_id=current.review_id,
            report_id=current.report_id,
            inspection_id=current.inspection_id,
            property_reference=current.property_reference,
            status=status,
            reason=current.reason,
            assigned_to=assigned_to if assigned_to is not None else current.assigned_to,
            resolution=resolution if resolution is not None else current.resolution,
            created_by=current.created_by,
            created_at=current.created_at,
            updated_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                staff_review_queue_records.update()
                .where(staff_review_queue_records.c.review_id == review_id)
                .values(**_staff_queue_values(updated))
            )
        return updated

    def get_staff_review_queue_item(self, review_id: str) -> StaffReviewQueueItem | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(staff_review_queue_records).where(
                    staff_review_queue_records.c.review_id == review_id
                )
            ).mappings().first()
        if row is None:
            return None
        return _row_to_staff_queue_item(row)

    def staff_review_summary(self) -> StaffReviewSummary:
        items = self.list_staff_review_queue_items()
        status_counts = Counter(item.status for item in items)
        return StaffReviewSummary(
            total_items=len(items),
            by_status=dict(sorted(status_counts.items())),
            open_items=sum(1 for item in items if item.status in OPEN_STAFF_REVIEW_STATUSES),
            generated_at=datetime.now(UTC),
        )


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


def _staff_queue_values(item: StaffReviewQueueItem) -> dict[str, object]:
    return {
        "review_id": item.review_id,
        "report_id": item.report_id,
        "inspection_id": item.inspection_id,
        "property_reference": item.property_reference,
        "status": item.status,
        "reason": item.reason,
        "assigned_to": item.assigned_to,
        "resolution": item.resolution,
        "created_by": item.created_by,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }


def _row_to_staff_queue_item(row: object) -> StaffReviewQueueItem:
    data = dict(row)
    return StaffReviewQueueItem(
        review_id=data["review_id"],
        report_id=data["report_id"],
        inspection_id=data["inspection_id"],
        property_reference=data["property_reference"],
        status=data["status"],
        reason=data["reason"],
        assigned_to=data["assigned_to"],
        resolution=data["resolution"],
        created_by=data["created_by"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )
