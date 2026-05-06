from app.core.constants import PaymentStatus
from app.core.exceptions import BusinessRuleError
from app.db.repositories.invoice_repository import InvoiceRepository
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.services.audit_service import AuditService
from app.services.cai_service import CaiService
from app.services.email_service import EmailService
from app.services.pdf_service import PdfService
from app.utils.formatters import fiscal_number
from app.utils.id_generator import new_id
from app.utils.money_utils import split_honduras_isv


class InvoiceService:
    def __init__(
        self,
        invoices: InvoiceRepository | None = None,
        cai_service: CaiService | None = None,
        pdf_service: PdfService | None = None,
        email_service: EmailService | None = None,
        audit_service: AuditService | None = None,
    ) -> None:
        self.invoices = invoices or InvoiceRepository()
        self.cai_service = cai_service or CaiService()
        self.pdf_service = pdf_service or PdfService()
        self.email_service = email_service or EmailService()
        self.audit_service = audit_service or AuditService()

    def generate_from_approved_payment(self, payment: Payment, customer_email: str | None = None) -> Invoice:
        if payment.status not in {PaymentStatus.APPROVED, PaymentStatus.COMPLETED}:
            raise BusinessRuleError("No se puede generar factura si BAC no aprobó el pago.")
        if payment.invoice_id:
            raise BusinessRuleError("Este pago ya tiene factura fiscal asociada.")

        cai, correlative = self.cai_service.consume_next_correlative()
        subtotal, isv, total = split_honduras_isv(payment.amount)
        number = fiscal_number(cai.establishment, cai.emission_point, cai.document_type, correlative)
        invoice = Invoice(
            id=new_id("invoice"),
            invoice_number=number,
            storeganise_invoice_id=payment.storeganise_invoice_id,
            payment_id=payment.payment_id,
            customer_id=payment.customer_id,
            cai_id=cai.id,
            cai=cai.cai,
            correlative=correlative,
            subtotal=subtotal,
            isv=isv,
            total=total,
        )
        invoice.pdf_url = self.pdf_service.generate_invoice_pdf(invoice)
        self.invoices.add(invoice)
        payment.invoice_id = invoice.id
        payment.status = PaymentStatus.COMPLETED
        if customer_email:
            self.email_service.send_invoice(invoice, customer_email)
        self.audit_service.record("Factura generada", "INVOICES", invoice.id, new_value={"invoice_number": invoice.invoice_number})
        return invoice

    def list(self) -> list[Invoice]:
        return self.invoices.list()

    def get(self, invoice_id: str) -> Invoice | None:
        return self.invoices.get(invoice_id)
