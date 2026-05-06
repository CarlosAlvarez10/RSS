from app.core.constants import AlertLevel, PaymentStatus
from app.services.alert_service import AlertService
from app.services.payment_service import PaymentService


def reconcile_pending_payments() -> dict:
    service = PaymentService()
    pending = [payment for payment in service.list() if payment.status == PaymentStatus.WAITING_BAC_CONFIRMATION]
    for payment in pending:
        AlertService().create(AlertLevel.WARNING, "Pago pendiente", "Pago BAC pendiente por demasiado tiempo.", "BAC", payment.payment_id)
    return {"status": "COMPLETED", "pending_checked": len(pending)}
