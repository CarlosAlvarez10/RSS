from dataclasses import dataclass, field
from app.core.constants import AlertLevel, AlertStatus
from app.utils.date_utils import iso_now


@dataclass
class Alert:
    id: str
    level: AlertLevel
    type: str
    message: str
    module: str
    reference_id: str | None = None
    status: AlertStatus = AlertStatus.PENDING
    created_at: str = field(default_factory=iso_now)
    resolved_at: str | None = None
