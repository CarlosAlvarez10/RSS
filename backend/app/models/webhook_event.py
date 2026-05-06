from dataclasses import dataclass, field
from app.utils.date_utils import iso_now


@dataclass
class WebhookEvent:
    id: str
    provider: str
    event_id: str
    event_type: str
    signature_valid: bool
    raw_payload: dict
    status: str = "RECEIVED"
    received_at: str = field(default_factory=iso_now)
    processed_at: str | None = None
    error_message: str | None = None
    retry_count: int = 0
