from dataclasses import dataclass, field
from app.core.constants import EmailStatus
from app.utils.date_utils import iso_now


@dataclass
class EmailLog:
    id: str
    invoice_id: str
    customer_id: str
    to_email: str
    subject: str
    status: EmailStatus = EmailStatus.PENDING
    sent_at: str | None = None
    error_message: str | None = None
    provider_response: dict = field(default_factory=dict)
    created_at: str = field(default_factory=iso_now)
