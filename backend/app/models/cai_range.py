from dataclasses import dataclass, field
from datetime import date
from app.core.constants import CaiStatus
from app.utils.date_utils import iso_now


@dataclass
class CaiRange:
    id: str
    cai: str
    range_start: int
    range_end: int
    current_number: int
    expiration_date: date
    authorization_date: date
    status: CaiStatus
    document_type: str
    establishment: str
    emission_point: str
    branch: str
    created_by: str = "system"
    created_at: str = field(default_factory=iso_now)
    updated_at: str = field(default_factory=iso_now)
