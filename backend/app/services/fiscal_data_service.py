from app.core.constants import InvoiceSourceStatus
from app.db.repositories.customer_repository import CustomerRepository
from app.db.repositories.invoice_repository import StoreganiseInvoiceRepository
from app.models.customer import Customer
from app.utils.date_utils import iso_now
from app.utils.id_generator import new_id


class FiscalDataService:
    def __init__(self, customers: CustomerRepository | None = None, source_invoices: StoreganiseInvoiceRepository | None = None) -> None:
        self.customers = customers or CustomerRepository()
        self.source_invoices = source_invoices or StoreganiseInvoiceRepository()

    def save_fiscal_data(self, storeganise_invoice_id: str, payload) -> Customer:
        customer = Customer(id=new_id("customer"), fiscal_status="COMPLETE", **payload.model_dump())
        self.customers.add(customer)
        source = self.source_invoices.get_by_storeganise_invoice_id(storeganise_invoice_id)
        if source:
            source.customer_id = customer.id
            source.internal_status = InvoiceSourceStatus.FISCAL_DATA_COMPLETED
            source.updated_at = iso_now()
        return customer
