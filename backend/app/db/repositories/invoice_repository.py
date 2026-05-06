from app.db.repositories.base_repository import BaseRepository


class InvoiceRepository(BaseRepository):
    table_name = "invoices"


class StoreganiseInvoiceRepository(BaseRepository):
    table_name = "storeganise_invoices"

    def get_by_storeganise_invoice_id(self, invoice_id: str):
        matches = self.find_by(storeganise_invoice_id=invoice_id)
        return matches[0] if matches else None
