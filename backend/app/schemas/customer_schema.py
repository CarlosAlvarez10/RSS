from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    customer_type: str
    email: EmailStr
    storeganise_user_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    company_name: str | None = None
    legal_name: str | None = None
    rtn: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None


class CustomerResponse(CustomerCreate):
    id: str
    fiscal_status: str
    created_at: str
    updated_at: str
