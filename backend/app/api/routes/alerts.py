from fastapi import APIRouter
from app.core.constants import AlertLevel, AlertStatus
from app.schemas.alert_schema import AlertCreate
from app.services.alert_service import AlertService


router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def list_alerts(level: AlertLevel | None = None, status: AlertStatus | None = None):
    return AlertService().list(level, status)


@router.post("")
def create_alert(payload: AlertCreate):
    return AlertService().create(**payload.model_dump())


@router.post("/{alert_id}/review")
def review_alert(alert_id: str):
    return AlertService().mark_in_review(alert_id)


@router.post("/{alert_id}/resolve")
def resolve_alert(alert_id: str):
    return AlertService().resolve(alert_id)
