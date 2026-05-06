from fastapi import APIRouter
from app.schemas.payment_schema import PaymentCreate
from app.services.payment_service import PaymentService


router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("")
def create_payment(payload: PaymentCreate):
    return PaymentService().create_payment(payload)


@router.get("")
def list_payments():
    return PaymentService().list()


@router.get("/{payment_id}")
def payment_detail(payment_id: str):
    service = PaymentService()
    return service.payments.get_by_payment_id(payment_id)


@router.post("/{payment_id}/retry")
def retry_validation(payment_id: str):
    return {"payment_id": payment_id, "status": "WAITING_BAC_CONFIRMATION"}


@router.post("/{payment_id}/review")
def mark_in_review(payment_id: str):
    return PaymentService().mark_in_review(payment_id)
