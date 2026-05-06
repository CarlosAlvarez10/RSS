from app.core.constants import AlertLevel, AlertStatus
from app.db.repositories.alert_repository import AlertRepository
from app.models.alert import Alert
from app.utils.date_utils import iso_now
from app.utils.id_generator import new_id


class AlertService:
    def __init__(self, alerts: AlertRepository | None = None) -> None:
        self.alerts = alerts or AlertRepository()

    def create(self, level: AlertLevel, type: str, message: str, module: str, reference_id: str | None = None) -> Alert:
        alert = Alert(id=new_id("alert"), level=level, type=type, message=message, module=module, reference_id=reference_id)
        return self.alerts.add(alert)

    def list(self, level: AlertLevel | None = None, status: AlertStatus | None = None) -> list[Alert]:
        items = self.alerts.list()
        if level:
            items = [item for item in items if item.level == level]
        if status:
            items = [item for item in items if item.status == status]
        return items

    def mark_in_review(self, alert_id: str) -> Alert | None:
        return self.alerts.update(alert_id, status=AlertStatus.IN_REVIEW)

    def resolve(self, alert_id: str) -> Alert | None:
        return self.alerts.update(alert_id, status=AlertStatus.RESOLVED, resolved_at=iso_now())

    def cai_expiring(self, cai_id: str, days: int) -> Alert:
        level = AlertLevel.CRITICAL if days <= 7 else AlertLevel.WARNING
        return self.create(level, "CAI por vencer", f"El CAI vence en {days} días.", "CAI", cai_id)

    def payment_failed(self, payment_id: str, message: str) -> Alert:
        return self.create(AlertLevel.CRITICAL, "Error BAC", message, "BAC", payment_id)
