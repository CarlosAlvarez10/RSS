from decimal import Decimal
from app.core.config import get_settings
from app.core.constants import PaymentStatus
from app.schemas.payment_schema import BacWebhookPayload
from app.utils.id_generator import new_id


class BacService:
    """BAC adapter. Currently simulator; keep interface when real API arrives."""

    def create_payment(self, payment_id: str, amount: Decimal, currency: str, customer_email: str | None = None) -> dict:
        transaction_id = new_id("bac_tx")
        reference = f"BAC-{transaction_id[-6:].upper()}"
        return {
            "payment_url": f"{get_settings().bac_simulator_base_url}/{payment_id}",
            "bac_transaction_id": transaction_id,
            "bac_reference": reference,
            "status": PaymentStatus.WAITING_BAC_CONFIRMATION,
            "amount": amount,
            "currency": currency,
            "customer_email": customer_email,
        }

    def validate_webhook(self, payload: BacWebhookPayload) -> bool:
        return bool(payload.payment_id and payload.bac_transaction_id and payload.bac_reference and payload.amount > 0)

    def get_payment_status(self, bac_transaction_id: str) -> dict:
        return {"bac_transaction_id": bac_transaction_id, "status": PaymentStatus.WAITING_BAC_CONFIRMATION}

    def refund_payment(self, bac_transaction_id: str) -> dict:
        return {"bac_transaction_id": bac_transaction_id, "status": PaymentStatus.REFUNDED}
