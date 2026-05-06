from decimal import Decimal
from pydantic import BaseModel, EmailStr
from app.core.constants import PaymentStatus


class PaymentCreate(BaseModel):
    storeganise_invoice_id: str
    customer_id: str
    amount: Decimal
    currency: str = "HNL"


class BacWebhookPayload(BaseModel):
    payment_id: str
    bac_transaction_id: str
    bac_reference: str
    amount: Decimal
    status: PaymentStatus
    customer_email: EmailStr | None = None
    raw_response: dict = {}


class PaymentResponse(BaseModel):
    payment_id: str
    status: PaymentStatus
    payment_url: str | None = None
    bac_transaction_id: str | None = None
    bac_reference: str | None = None
    invoice_id: str | None = None
