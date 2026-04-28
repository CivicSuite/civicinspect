"""FastAPI runtime foundation for CivicInspect."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicinspect import __version__
from civicinspect.case_lookup import lookup_repeat_cases
from civicinspect.notice_draft import draft_notice
from civicinspect.persistence import InspectionCaseRepository, StoredInspectionReport
from civicinspect.public_ui import render_public_lookup_page
from civicinspect.records_export import build_inspection_export
from civicinspect.report_draft import draft_inspection_report


app = FastAPI(
    title="CivicInspect",
    version=__version__,
    description="Inspection report, repeat-case, and notice-drafting support for CivicSuite.",
)

_case_repository: InspectionCaseRepository | None = None
_case_db_url: str | None = None


class RepeatCaseLookupRequest(BaseModel):
    property_reference: str
    violation_type: str = ""


class ReportDraftRequest(BaseModel):
    inspection_id: str
    property_reference: str
    inspector_notes: str
    photo_observations: list[str] = []
    voice_notes: str = ""


class NoticeDraftRequest(BaseModel):
    case_id: str
    property_reference: str
    violation_type: str
    observations: list[str]


class InspectionExportRequest(BaseModel):
    title: str
    case_id: str
    format: str = "markdown"


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicInspect",
        "version": __version__,
        "status": "inspection support foundation plus case persistence",
        "message": (
            "CivicInspect package, API foundation, sample repeat-case lookup, optional database-backed repeat-case and report-draft records, inspector-owned "
            "report draft helper, notice draft helper, records-ready export checklist, and public UI "
            "foundation are online; official findings, citations, fines, inspection scheduling, live "
            "photo analysis, live LLM calls, and system-of-record integrations are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: local inspection configuration, CivicCode context APIs, and staff review queues",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civicinspect",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civicinspect", response_class=HTMLResponse)
def public_civicinspect_page() -> str:
    """Return the public sample inspection support UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civicinspect/cases/repeat-lookup")
def repeat_case_lookup(request: RepeatCaseLookupRequest) -> dict[str, object]:
    result = _lookup_repeat_cases(
        property_reference=request.property_reference,
        violation_type=request.violation_type,
    )
    return result.__dict__


@app.post("/api/v1/civicinspect/reports/draft")
def inspection_report_draft(request: ReportDraftRequest) -> dict[str, object]:
    if _case_database_url() is not None:
        stored = _get_case_repository().create_report(
            inspection_id=request.inspection_id,
            property_reference=request.property_reference,
            inspector_notes=request.inspector_notes,
            photo_observations=tuple(request.photo_observations),
            voice_notes=request.voice_notes,
        )
        return _stored_report_response(stored)

    result = draft_inspection_report(
        inspection_id=request.inspection_id,
        property_reference=request.property_reference,
        inspector_notes=request.inspector_notes,
        photo_observations=tuple(request.photo_observations),
        voice_notes=request.voice_notes,
    )
    payload = result.__dict__
    payload["report_id"] = None
    return payload


@app.get("/api/v1/civicinspect/reports/{report_id}")
def get_inspection_report(report_id: str) -> dict[str, object]:
    if _case_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicInspect case persistence is not configured.",
                "fix": "Set CIVICINSPECT_CASE_DB_URL to retrieve persisted inspection report records.",
            },
        )
    stored = _get_case_repository().get_report(report_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Inspection report record not found.",
                "fix": "Use a report_id returned by POST /api/v1/civicinspect/reports/draft.",
            },
        )
    return _stored_report_response(stored)


@app.post("/api/v1/civicinspect/notices/draft")
def notice_draft(request: NoticeDraftRequest) -> dict[str, object]:
    result = draft_notice(
        case_id=request.case_id,
        property_reference=request.property_reference,
        violation_type=request.violation_type,
        observations=tuple(request.observations),
    )
    return result.__dict__


@app.post("/api/v1/civicinspect/export")
def inspection_export(request: InspectionExportRequest) -> dict[str, object]:
    result = build_inspection_export(
        title=request.title,
        case_id=request.case_id,
        format=request.format,
    )
    return result.__dict__


def _case_database_url() -> str | None:
    return os.environ.get("CIVICINSPECT_CASE_DB_URL")


def _get_case_repository() -> InspectionCaseRepository:
    global _case_db_url, _case_repository
    db_url = _case_database_url()
    if db_url is None:
        raise RuntimeError("CIVICINSPECT_CASE_DB_URL is not configured.")
    if _case_repository is None or db_url != _case_db_url:
        _dispose_case_repository()
        _case_db_url = db_url
        _case_repository = InspectionCaseRepository(db_url=db_url)
    return _case_repository


def _dispose_case_repository() -> None:
    global _case_repository
    if _case_repository is not None:
        _case_repository.engine.dispose()
        _case_repository = None


def _lookup_repeat_cases(*, property_reference: str, violation_type: str = ""):
    if _case_database_url() is None:
        return lookup_repeat_cases(property_reference=property_reference, violation_type=violation_type)
    return _get_case_repository().lookup_repeat_cases(
        property_reference=property_reference,
        violation_type=violation_type,
    )


def _stored_report_response(stored: StoredInspectionReport) -> dict[str, object]:
    return {
        "report_id": stored.report_id,
        "inspection_id": stored.inspection_id,
        "property_reference": stored.property_reference,
        "summary": stored.summary,
        "observation_bullets": list(stored.observation_bullets),
        "inspector_review_required": stored.inspector_review_required,
        "disclaimer": stored.disclaimer,
        "created_at": stored.created_at.isoformat(),
    }
