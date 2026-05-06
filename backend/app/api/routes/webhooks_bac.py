from fastapi import APIRouter, Depends, Request
from app.core.security import verify_bac_signature
from app.schemas.payment_schema import BacWebhookPayload
from app.services.payment_service import PaymentService


router = APIRouter(prefix="/webhooks/bac", tags=["webhooks-bac"])


@router.post("")
async def receive_bac_webhook(payload: BacWebhookPayload, _: bytes = Depends(verify_bac_signature)):
    payment = PaymentService().process_bac_confirmation(payload)
    return {"ok": True, "payment_id": payment.payment_id, "status": payment.status}


@router.post("/simulate")
async def simulate_bac_webhook(payload: BacWebhookPayload, request: Request):
    payment = PaymentService().process_bac_confirmation(payload)
    return {"ok": True, "simulated": True, "payment_id": payment.payment_id, "status": payment.status}
