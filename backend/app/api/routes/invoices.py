from fastapi import APIRouter, Query
from app.services.email_service import EmailService
from app.services.invoice_service import InvoiceService


router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("")
def list_invoices(date_from: str | None = None, date_to: str | None = None, client: str | None = None, rtn: str | None = None, cai: str | None = None, bac_reference: str | None = None):
    return InvoiceService().list()


@router.get("/{invoice_id}")
def invoice_detail(invoice_id: str):
    return InvoiceService().get(invoice_id)


@router.get("/{invoice_id}/pdf")
def download_pdf(invoice_id: str):
    invoice = InvoiceService().get(invoice_id)
    return {"invoice_id": invoice_id, "pdf_url": getattr(invoice, "pdf_url", None)}


@router.post("/{invoice_id}/resend")
def resend_email(invoice_id: str, to_email: str = Query(...)):
    invoice = InvoiceService().get(invoice_id)
    return EmailService().send_invoice(invoice, to_email) if invoice else None


@router.get("/exports/accountant")
def export_accountant():
    return {"status": "READY", "format": "CSV", "description": "Facturas fiscales emitidas para contador."}
