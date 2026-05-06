from app.db.repositories.alert_repository import AlertRepository
from app.db.repositories.cai_repository import CaiRepository
from app.db.repositories.invoice_repository import InvoiceRepository
from app.db.repositories.payment_repository import PaymentRepository


class ReportService:
    def __init__(self) -> None:
        self.invoices = InvoiceRepository()
        self.payments = PaymentRepository()
        self.cai_ranges = CaiRepository()
        self.alerts = AlertRepository()

    def invoices_for_accountant(self, filters: dict | None = None) -> list[dict]:
        return [self.invoices.to_dict(invoice) for invoice in self.invoices.list()]

    def payments_report(self) -> list[dict]:
        return [self.payments.to_dict(payment) for payment in self.payments.list()]

    def cai_report(self) -> list[dict]:
        return [self.cai_ranges.to_dict(cai) for cai in self.cai_ranges.list()]

    def errors_report(self) -> list[dict]:
        return [self.alerts.to_dict(alert) for alert in self.alerts.list()]

    def export(self, report_type: str, format: str = "json") -> dict:
        return {"report_type": report_type, "format": format, "status": "READY"}
