from dataclasses import dataclass, field
from decimal import Decimal
from app.core.constants import PaymentStatus
from app.utils.date_utils import iso_now


@dataclass
class Payment:
    id: str
    payment_id: str
    storeganise_invoice_id: str
    customer_id: str
    amount: Decimal
    currency: str = "HNL"
    status: PaymentStatus = PaymentStatus.PAYMENT_CREATED
    provider: str = "BAC"
    payment_url: str | None = None
    bac_transaction_id: str | None = None
    bac_reference: str | None = None
    invoice_id: str | None = None
    created_at: str = field(default_factory=iso_now)
    paid_at: str | None = None
    error_message: str | None = None
    raw_bac_response: dict = field(default_factory=dict)
