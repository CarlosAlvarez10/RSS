class BusinessRuleError(Exception):
    """Raised when a business rule blocks an operation."""


class DuplicateEventError(BusinessRuleError):
    """Raised when a webhook or payment was already processed."""


class FiscalLockError(BusinessRuleError):
    """Raised when a CAI range cannot be locked safely."""


class ExternalProviderError(Exception):
    """Raised when BAC, Storeganise, email or PDF provider fails."""
