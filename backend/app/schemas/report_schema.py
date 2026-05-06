from pydantic import BaseModel


class ReportFilters(BaseModel):
    date_from: str | None = None
    date_to: str | None = None
    customer: str | None = None
    rtn: str | None = None
    status: str | None = None
    cai: str | None = None


class ReportRequestSchema(BaseModel):
    report_type: str
    filters: ReportFilters = ReportFilters()
