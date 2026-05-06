from fastapi import APIRouter
from app.db.repositories.invoice_repository import StoreganiseInvoiceRepository
from app.db.repositories.webhook_repository import WebhookRepository
from app.services.storeganise_service import StoreganiseService


router = APIRouter(prefix="/storeganise", tags=["storeganise"])


@router.get("/events")
def list_events():
    return WebhookRepository().list()


@router.get("/invoices")
def list_storeganise_invoices():
    return StoreganiseInvoiceRepository().list()


@router.post("/sync/{storeganise_invoice_id}")
def sync_invoice(storeganise_invoice_id: str):
    return StoreganiseService().sync_after_payment(storeganise_invoice_id)
