from enum import StrEnum


ALERT_RECIPIENTS = ["admin@roatanselfstorage.com", "contador@roatanselfstorage.com"]
SUPPORTED_STOREGANISE_EVENTS = {
    "unitRental.invoice.created",
    "invoice.updated",
    "invoice.state.updated",
    "invoice.payments.updated",
    "user.created",
    "user.updated",
    "user.billing.updated",
    "addon.dailyEvent.started",
}


class PaymentStatus(StrEnum):
    PAYMENT_CREATED = "PAYMENT_CREATED"
    WAITING_BAC_CONFIRMATION = "WAITING_BAC_CONFIRMATION"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    DUPLICATE_BLOCKED = "DUPLICATE_BLOCKED"
    COMPLETED = "COMPLETED"


class InvoiceSourceStatus(StrEnum):
    STOREGANISE_RECEIVED = "STOREGANISE_RECEIVED"
    WAITING_FISCAL_DATA = "WAITING_FISCAL_DATA"
    FISCAL_DATA_COMPLETED = "FISCAL_DATA_COMPLETED"
    READY_FOR_PAYMENT = "READY_FOR_PAYMENT"
    PAYMENT_CREATED = "PAYMENT_CREATED"
    WAITING_BAC_CONFIRMATION = "WAITING_BAC_CONFIRMATION"
    BAC_APPROVED = "BAC_APPROVED"
    BAC_REJECTED = "BAC_REJECTED"
    BAC_FAILED = "BAC_FAILED"
    INVOICE_GENERATED = "INVOICE_GENERATED"
    EMAIL_SENT = "EMAIL_SENT"
    STOREGANISE_UPDATED = "STOREGANISE_UPDATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class CaiStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"
    EXHAUSTED = "EXHAUSTED"
    BLOCKED = "BLOCKED"


class EmailStatus(StrEnum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class AlertLevel(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlertStatus(StrEnum):
    PENDING = "PENDING"
    IN_REVIEW = "IN_REVIEW"
    RESOLVED = "RESOLVED"
    IGNORED = "IGNORED"
