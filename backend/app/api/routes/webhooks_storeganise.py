import json
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from app.core.security import verify_storeganise_signature
from app.schemas.webhook_schema import WebhookAccepted
from app.services.storeganise_service import StoreganiseService


router = APIRouter(prefix="/webhooks/storeganise", tags=["webhooks-storeganise"])


@router.post("", response_model=WebhookAccepted)
async def receive_storeganise_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    raw_body: bytes = Depends(verify_storeganise_signature),
):
    payload = json.loads(raw_body.decode("utf-8") or "{}")
    service = StoreganiseService()
    event = service.register_webhook(payload, signature_valid=True)
    background_tasks.add_task(service.process_event, event)
    return WebhookAccepted(event_id=event.event_id, status="ACCEPTED")
