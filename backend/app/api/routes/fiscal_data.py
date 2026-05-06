from fastapi import APIRouter
from app.schemas.customer_schema import CustomerCreate
from app.services.fiscal_data_service import FiscalDataService


router = APIRouter(prefix="/fiscal-data", tags=["fiscal-data"])


@router.post("/{storeganise_invoice_id}")
def save_fiscal_data(storeganise_invoice_id: str, payload: CustomerCreate):
    return FiscalDataService().save_fiscal_data(storeganise_invoice_id, payload)
