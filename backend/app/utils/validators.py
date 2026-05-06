from decimal import Decimal
from app.core.exceptions import BusinessRuleError


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BusinessRuleError(message)


def amounts_match(expected: Decimal, actual: Decimal) -> bool:
    return expected.quantize(Decimal("0.01")) == actual.quantize(Decimal("0.01"))
