from dataclasses import dataclass, field
from app.utils.date_utils import iso_now


@dataclass
class ReportRequest:
    id: str
    report_type: str
    filters: dict
    generated_by: str = "system"
    created_at: str = field(default_factory=iso_now)
