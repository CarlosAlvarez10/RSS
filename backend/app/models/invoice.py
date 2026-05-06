from dataclasses import dataclass, field
from decimal import Decimal
from app.core.constants import EmailStatus, InvoiceSourceStatus
from app.utils.date_utils import iso_now


@dataclass
class StoreganiseInvoice:
    id: str
    storeganise_invoice_id: str
    storeganise_user_id: str | None
    customer_id: str | None
    amount: Decimal
    currency: str = "HNL"
    status: str = "OPEN"
    internal_status: InvoiceSourceStatus = InvoiceSourceStatus.STOREGANISE_RECEIVED
    raw_payload: dict = field(default_factory=dict)
    created_at: str = field(default_factory=iso_now)
    updated_at: str = field(default_factory=iso_now)


@dataclass
class Invoice:
    id: str
    invoice_number: str
    storeganise_invoice_id: str
    payment_id: str
    customer_id: str
    cai_id: str
    cai: str
    correlative: int
    subtotal: Decimal
    isv: Decimal
    total: Decimal
    pdf_url: str | None = None
    email_status: EmailStatus = EmailStatus.PENDING
    status: str = "ISSUED"
    issued_at: str = field(default_factory=iso_now)
    created_at: str = field(default_factory=iso_now)
