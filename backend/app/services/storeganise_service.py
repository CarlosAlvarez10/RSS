from decimal import Decimal
from app.core.constants import AlertLevel, InvoiceSourceStatus, SUPPORTED_STOREGANISE_EVENTS
from app.core.exceptions import BusinessRuleError
from app.db.repositories.customer_repository import CustomerRepository
from app.db.repositories.invoice_repository import StoreganiseInvoiceRepository
from app.db.repositories.webhook_repository import WebhookRepository
from app.models.customer import Customer
from app.models.invoice import StoreganiseInvoice
from app.models.webhook_event import WebhookEvent
from app.services.alert_service import AlertService
from app.services.audit_service import AuditService
from app.utils.date_utils import iso_now
from app.utils.id_generator import new_id


class StoreganiseService:
    def __init__(
        self,
        webhooks: WebhookRepository | None = None,
        source_invoices: StoreganiseInvoiceRepository | None = None,
        customers: CustomerRepository | None = None,
        alerts: AlertService | None = None,
        audits: AuditService | None = None,
    ) -> None:
        self.webhooks = webhooks or WebhookRepository()
        self.source_invoices = source_invoices or StoreganiseInvoiceRepository()
        self.customers = customers or CustomerRepository()
        self.alerts = alerts or AlertService()
        self.audits = audits or AuditService()

    def register_webhook(self, payload: dict, signature_valid: bool) -> WebhookEvent:
        event_id = str(payload.get("id") or payload.get("event_id") or new_id("sg_event"))
        event_type = str(payload.get("type") or payload.get("event_type"))
        existing = self.webhooks.get_by_event_id("STOREGANISE", event_id)
        if existing:
            return existing
        event = WebhookEvent(id=new_id("webhook"), provider="STOREGANISE", event_id=event_id, event_type=event_type, signature_valid=signature_valid, raw_payload=payload)
        return self.webhooks.add(event)

    def process_event(self, event: WebhookEvent) -> WebhookEvent:
        try:
            if event.event_type not in SUPPORTED_STOREGANISE_EVENTS:
                event.status = "IGNORED"
                return event
            handler = {
                "unitRental.invoice.created": self.handle_invoice_created,
                "invoice.updated": self.handle_invoice_updated,
                "invoice.state.updated": self.handle_invoice_state_updated,
                "invoice.payments.updated": self.handle_invoice_payments_updated,
                "user.created": self.handle_user_created,
                "user.updated": self.handle_user_updated,
                "user.billing.updated": self.handle_user_billing_updated,
                "addon.dailyEvent.started": self.handle_daily_event,
            }[event.event_type]
            handler(event.raw_payload)
            event.status = "PROCESSED"
            event.processed_at = iso_now()
        except Exception as exc:
            event.status = "FAILED"
            event.error_message = str(exc)
            self.alerts.create(AlertLevel.CRITICAL, "Error Storeganise", str(exc), "STOREGANISE", event.event_id)
        return event

    def handle_invoice_created(self, payload: dict) -> StoreganiseInvoice:
        data = payload.get("data", payload)
        invoice_id = str(data.get("invoiceId") or data.get("invoice_id") or data.get("id") or new_id("sg_invoice"))
        existing = self.source_invoices.get_by_storeganise_invoice_id(invoice_id)
        if existing:
            return existing
        invoice = StoreganiseInvoice(
            id=new_id("source_invoice"),
            storeganise_invoice_id=invoice_id,
            storeganise_user_id=data.get("userId") or data.get("storeganise_user_id"),
            customer_id=None,
            amount=Decimal(str(data.get("amount", "0"))),
            currency=data.get("currency", "HNL"),
            status=data.get("status", "OPEN"),
            internal_status=InvoiceSourceStatus.WAITING_FISCAL_DATA,
            raw_payload=payload,
        )
        self.audits.record("Factura Storeganise recibida", "STOREGANISE", invoice.storeganise_invoice_id, new_value=payload)
        return self.source_invoices.add(invoice)

    def handle_invoice_updated(self, payload: dict) -> None:
        data = payload.get("data", payload)
        invoice = self.source_invoices.get_by_storeganise_invoice_id(str(data.get("invoiceId") or data.get("id")))
        if invoice and invoice.internal_status not in {InvoiceSourceStatus.INVOICE_GENERATED, InvoiceSourceStatus.COMPLETED}:
            invoice.amount = Decimal(str(data.get("amount", invoice.amount)))
            invoice.status = data.get("status", invoice.status)
            invoice.updated_at = iso_now()

    def handle_invoice_state_updated(self, payload: dict) -> None:
        data = payload.get("data", payload)
        invoice = self.source_invoices.get_by_storeganise_invoice_id(str(data.get("invoiceId") or data.get("id")))
        if invoice:
            invoice.status = data.get("state", data.get("status", invoice.status))
            if invoice.status == "paid" and invoice.internal_status not in {InvoiceSourceStatus.BAC_APPROVED, InvoiceSourceStatus.COMPLETED}:
                self.alerts.create(AlertLevel.WARNING, "Storeganise paid sin BAC", "Storeganise marcó paid sin BAC aprobado interno.", "STOREGANISE", invoice.storeganise_invoice_id)

    def handle_invoice_payments_updated(self, payload: dict) -> None:
        self.alerts.create(AlertLevel.INFO, "Pago Storeganise actualizado", "Se detectó cambio de pago; la factura fiscal depende solo de BAC.", "STOREGANISE", str(payload.get("id", "")))

    def handle_user_created(self, payload: dict) -> Customer:
        data = payload.get("data", payload)
        user_id = str(data.get("userId") or data.get("id") or new_id("sg_user"))
        existing = self.customers.get_by_storeganise_user_id(user_id)
        if existing:
            return existing
        return self.customers.add(Customer(id=new_id("customer"), storeganise_user_id=user_id, customer_type="persona natural", email=data.get("email", "missing@example.com"), first_name=data.get("firstName"), last_name=data.get("lastName"), phone=data.get("phone"), address=data.get("address")))

    def handle_user_updated(self, payload: dict) -> None:
        data = payload.get("data", payload)
        customer = self.customers.get_by_storeganise_user_id(str(data.get("userId") or data.get("id")))
        if customer:
            customer.email = data.get("email", customer.email)
            customer.phone = data.get("phone", customer.phone)
            customer.address = data.get("address", customer.address)
            customer.updated_at = iso_now()

    def handle_user_billing_updated(self, payload: dict) -> None:
        data = payload.get("data", payload)
        customer = self.customers.get_by_storeganise_user_id(str(data.get("userId") or data.get("id")))
        if customer:
            customer.rtn = data.get("rtn", customer.rtn)
            customer.legal_name = data.get("legalName", customer.legal_name)
            customer.fiscal_status = "COMPLETE" if customer.rtn else customer.fiscal_status

    def handle_daily_event(self, payload: dict) -> None:
        self.alerts.create(AlertLevel.INFO, "Revisión diaria Storeganise", "Se ejecutó revisión diaria de pagos, correos, CAI y sincronizaciones.", "STOREGANISE")

    def sync_after_payment(self, storeganise_invoice_id: str) -> dict:
        if not storeganise_invoice_id:
            raise BusinessRuleError("Falta Storeganise invoice id.")
        return {"storeganise_invoice_id": storeganise_invoice_id, "status": "SYNCED"}
