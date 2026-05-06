from app.services.alert_service import AlertService


def notify_alert_recipients(alert_id: str) -> dict:
    return {"alert_id": alert_id, "notified": True}


def create_manual_alert(level: str, message: str) -> dict:
    alert = AlertService().create(level=level, type="Manual", message=message, module="SYSTEM")
    return {"alert_id": alert.id}
