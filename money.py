from argparse import ArgumentTypeError
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def amount(text):
    try:
        value = Decimal(text.replace(",", "."))
    except InvalidOperation:
        raise ArgumentTypeError("Введите число") from None
    if not value.is_finite() or value < 0 or value > 10**9 or value.as_tuple().exponent < -6:
        raise ArgumentTypeError("Введите число от 0 до 1 млрд, до 6 знаков после запятой")
    return value


def money(value):
    return f"{value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} руб."
