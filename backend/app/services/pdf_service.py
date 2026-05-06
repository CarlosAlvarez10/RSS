from app.models.invoice import Invoice


class PdfService:
    def generate_invoice_pdf(self, invoice: Invoice, customer: object | None = None) -> str:
        # Production: render HTML template with logo, CAI, range, BAC reference and totals, then store PDF.
        return f"/generated/invoices/{invoice.invoice_number}.pdf"
