from datetime import date
from pydantic import BaseModel
from app.core.constants import CaiStatus


class CaiCreate(BaseModel):
    cai: str
    range_start: int
    range_end: int
    current_number: int
    expiration_date: date
    authorization_date: date
    document_type: str = "01"
    establishment: str = "001"
    emission_point: str = "002"
    branch: str = "001"
    created_by: str = "admin"
    status: CaiStatus = CaiStatus.INACTIVE


class CaiResponse(CaiCreate):
    id: str
    available: int
    used: int
