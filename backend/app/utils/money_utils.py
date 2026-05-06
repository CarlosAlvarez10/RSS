from decimal import Decimal, ROUND_HALF_UP


TAX_RATE = Decimal("0.15")


def money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def split_honduras_isv(total: Decimal | int | float | str) -> tuple[Decimal, Decimal, Decimal]:
    total_amount = money(total)
    subtotal = money(total_amount / (Decimal("1.00") + TAX_RATE))
    isv = money(total_amount - subtotal)
    return subtotal, isv, total_amount
