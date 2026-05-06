from dataclasses import dataclass, field
from app.utils.date_utils import iso_now


@dataclass
class Customer:
    id: str
    customer_type: str
    email: str
    storeganise_user_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    company_name: str | None = None
    legal_name: str | None = None
    rtn: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    fiscal_status: str = "INCOMPLETE"
    created_at: str = field(default_factory=iso_now)
    updated_at: str = field(default_factory=iso_now)
