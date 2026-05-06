from fastapi import APIRouter
from app.schemas.report_schema import ReportRequestSchema
from app.services.report_service import ReportService


router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("")
def generate_report(payload: ReportRequestSchema):
    service = ReportService()
    if payload.report_type == "payments":
        return service.payments_report()
    if payload.report_type == "cai":
        return service.cai_report()
    if payload.report_type == "errors":
        return service.errors_report()
    return service.invoices_for_accountant(payload.filters.model_dump())


@router.get("/export")
def export_report(report_type: str, format: str = "csv"):
    return ReportService().export(report_type, format)
