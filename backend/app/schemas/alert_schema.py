from pydantic import BaseModel
from app.core.constants import AlertLevel, AlertStatus


class AlertCreate(BaseModel):
    level: AlertLevel
    type: str
    message: str
    module: str
    reference_id: str | None = None


class AlertResponse(AlertCreate):
    id: str
    status: AlertStatus
    created_at: str
    resolved_at: str | None = None
