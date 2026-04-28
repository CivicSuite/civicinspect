"""FastAPI runtime foundation for CivicInspect."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicinspect import __version__
from civicinspect.case_lookup import lookup_repeat_cases
from civicinspect.notice_draft import draft_notice
from civicinspect.public_ui import render_public_lookup_page
from civicinspect.records_export import build_inspection_export
from civicinspect.report_draft import draft_inspection_report


app = FastAPI(
    title="CivicInspect",
    version=__version__,
    description="Inspection report, repeat-case, and notice-drafting support for CivicSuite.",
)


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
        "status": "inspection support foundation",
        "message": (
            "CivicInspect package, API foundation, sample repeat-case lookup, inspector-owned "
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
    result = lookup_repeat_cases(
        property_reference=request.property_reference,
        violation_type=request.violation_type,
    )
    return result.__dict__


@app.post("/api/v1/civicinspect/reports/draft")
def inspection_report_draft(request: ReportDraftRequest) -> dict[str, object]:
    result = draft_inspection_report(
        inspection_id=request.inspection_id,
        property_reference=request.property_reference,
        inspector_notes=request.inspector_notes,
        photo_observations=tuple(request.photo_observations),
        voice_notes=request.voice_notes,
    )
    return result.__dict__


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
