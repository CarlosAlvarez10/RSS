from fastapi import APIRouter
from app.services.email_service import EmailLogRepository


router = APIRouter(prefix="/email-logs", tags=["email-logs"])


@router.get("")
def list_email_logs():
    return EmailLogRepository().list()
