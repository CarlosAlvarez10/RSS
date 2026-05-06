from app.db.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository):
    table_name = "payments"

    def get_by_payment_id(self, payment_id: str):
        matches = self.find_by(payment_id=payment_id)
        return matches[0] if matches else None

    def get_by_bac_transaction_id(self, transaction_id: str):
        matches = self.find_by(bac_transaction_id=transaction_id)
        return matches[0] if matches else None
