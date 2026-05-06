from decimal import Decimal
from pydantic import BaseModel


class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    storeganise_invoice_id: str
    payment_id: str
    customer_id: str
    cai: str
    correlative: int
    subtotal: Decimal
    isv: Decimal
    total: Decimal
    pdf_url: str | None
    email_status: str
    status: str
    issued_at: str
