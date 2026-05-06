from app.services.storeganise_service import StoreganiseService


class SyncService:
    def __init__(self, storeganise_service: StoreganiseService | None = None) -> None:
        self.storeganise_service = storeganise_service or StoreganiseService()

    def sync_invoice_after_payment(self, storeganise_invoice_id: str) -> dict:
        return self.storeganise_service.sync_after_payment(storeganise_invoice_id)
