from app.core.constants import AlertLevel, EmailStatus
from app.db.repositories.base_repository import BaseRepository
from app.models.email_log import EmailLog
from app.models.invoice import Invoice
from app.services.alert_service import AlertService
from app.utils.date_utils import iso_now
from app.utils.id_generator import new_id


class EmailLogRepository(BaseRepository):
    table_name = "email_logs"


class EmailService:
    def __init__(self, logs: EmailLogRepository | None = None, alerts: AlertService | None = None) -> None:
        self.logs = logs or EmailLogRepository()
        self.alerts = alerts or AlertService()

    def send_invoice(self, invoice: Invoice, to_email: str) -> EmailLog:
        log = EmailLog(id=new_id("email"), invoice_id=invoice.id, customer_id=invoice.customer_id, to_email=to_email, subject=f"Factura {invoice.invoice_number}")
        try:
            log.status = EmailStatus.SENT
            log.sent_at = iso_now()
            log.provider_response = {"accepted": True, "provider": "simulated"}
            invoice.email_status = EmailStatus.SENT
        except Exception as exc:
            log.status = EmailStatus.FAILED
            log.error_message = str(exc)
            invoice.email_status = EmailStatus.FAILED
            self.alerts.create(AlertLevel.WARNING, "Correo fallido", str(exc), "EMAIL", invoice.id)
        return self.logs.add(log)

    def retry_failed(self) -> list[EmailLog]:
        retried = []
        for log in self.logs.find_by(status=EmailStatus.FAILED):
            log.status = EmailStatus.RETRYING
            retried.append(log)
        return retried
