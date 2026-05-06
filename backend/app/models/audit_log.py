from dataclasses import dataclass, field
from app.utils.date_utils import iso_now


@dataclass
class AuditLog:
    id: str
    action: str
    module: str
    entity_id: str
    user_id: str = "system"
    old_value: dict | None = None
    new_value: dict | None = None
    ip_address: str | None = None
    created_at: str = field(default_factory=iso_now)
