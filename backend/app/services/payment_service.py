from decimal import Decimal
from app.core.constants import AlertLevel, PaymentStatus
from app.core.exceptions import BusinessRuleError, DuplicateEventError
from app.db.repositories.customer_repository import CustomerRepository
from app.db.repositories.payment_repository import PaymentRepository
from app.models.payment import Payment
from app.schemas.payment_schema import BacWebhookPayload, PaymentCreate
from app.services.alert_service import AlertService
from app.services.audit_service import AuditService
from app.services.bac_service import BacService
from app.services.invoice_service import InvoiceService
from app.utils.date_utils import iso_now
from app.utils.id_generator import new_id
from app.utils.validators import amounts_match


class PaymentService:
    def __init__(
        self,
        payments: PaymentRepository | None = None,
        customers: CustomerRepository | None = None,
        bac_service: BacService | None = None,
        invoice_service: InvoiceService | None = None,
        alerts: AlertService | None = None,
        audits: AuditService | None = None,
    ) -> None:
        self.payments = payments or PaymentRepository()
        self.customers = customers or CustomerRepository()
        self.bac_service = bac_service or BacService()
        self.invoice_service = invoice_service or InvoiceService()
        self.alerts = alerts or AlertService()
        self.audits = audits or AuditService()

    def create_payment(self, payload: PaymentCreate) -> Payment:
        payment_id = new_id("payment")
        payment = Payment(id=new_id("payrow"), payment_id=payment_id, storeganise_invoice_id=payload.storeganise_invoice_id, customer_id=payload.customer_id, amount=payload.amount, currency=payload.currency)
        bac_response = self.bac_service.create_payment(payment_id, payload.amount, payload.currency)
        payment.payment_url = bac_response["payment_url"]
        payment.bac_transaction_id = bac_response["bac_transaction_id"]
        payment.bac_reference = bac_response["bac_reference"]
        payment.status = PaymentStatus.WAITING_BAC_CONFIRMATION
        payment.raw_bac_response = bac_response
        self.payments.add(payment)
        self.audits.record("Pago BAC creado", "PAYMENTS", payment.payment_id, new_value=bac_response)
        return payment

    def process_bac_confirmation(self, payload: BacWebhookPayload) -> Payment:
        if not self.bac_service.validate_webhook(payload):
            raise BusinessRuleError("Webhook BAC inválido.")
        payment = self.payments.get_by_payment_id(payload.payment_id)
        if not payment:
            raise BusinessRuleError("payment_id no existe.")
        duplicate = self.payments.get_by_bac_transaction_id(payload.bac_transaction_id)
        if duplicate and duplicate.payment_id != payment.payment_id and duplicate.status in {PaymentStatus.APPROVED, PaymentStatus.COMPLETED}:
            payment.status = PaymentStatus.DUPLICATE_BLOCKED
            raise DuplicateEventError("Pago ya procesado anteriormente.")
        if payment.status == PaymentStatus.COMPLETED:
            return payment
        if not amounts_match(Decimal(payment.amount), Decimal(payload.amount)):
            payment.status = PaymentStatus.FAILED
            payment.error_message = "Monto BAC no coincide con monto interno."
            self.alerts.create(AlertLevel.CRITICAL, "Monto no coincide", payment.error_message, "BAC", payment.payment_id)
            return payment

        payment.bac_transaction_id = payload.bac_transaction_id
        payment.bac_reference = payload.bac_reference
        payment.raw_bac_response = payload.raw_response
        payment.paid_at = iso_now() if payload.status == PaymentStatus.APPROVED else None

        if payload.status == PaymentStatus.APPROVED:
            payment.status = PaymentStatus.APPROVED
            customer = self.customers.get(payment.customer_id)
            self.invoice_service.generate_from_approved_payment(payment, getattr(customer, "email", None) or payload.customer_email)
        elif payload.status == PaymentStatus.REJECTED:
            payment.status = PaymentStatus.REJECTED
            self.alerts.create(AlertLevel.WARNING, "Pago BAC rechazado", "BAC rechazó la transacción.", "BAC", payment.payment_id)
        else:
            payment.status = PaymentStatus.FAILED
            self.alerts.create(AlertLevel.CRITICAL, "Pago BAC fallido", "BAC reportó una falla.", "BAC", payment.payment_id)

        self.audits.record("Confirmación BAC procesada", "PAYMENTS", payment.payment_id, new_value={"status": payment.status})
        return payment

    def list(self) -> list[Payment]:
        return self.payments.list()

    def mark_in_review(self, payment_id: str) -> Payment | None:
        payment = self.payments.get_by_payment_id(payment_id)
        if payment:
            payment.error_message = "Pago marcado en revisión manual."
        return payment
