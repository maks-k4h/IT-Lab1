import re

from .data_type import DataType


class Money(DataType):
    MAX_VALUE = 10_000_000_000_000 * 100  # Maximum value in cents (10 trillion)

    def __init__(self, amount_cents: int):
        self._value = amount_cents

    def __str__(self) -> str:
        dollars = self._value // 100
        cents = self._value % 100
        return f"${dollars}.{cents:02d}"

    @staticmethod
    def from_string(value: str) -> 'Money':
        pattern = r'^\$\d+(\.\d{2})?$'
        if re.match(pattern, value):
            amount_str = value.replace('$', '')
            if '.' in amount_str:
                dollars, cents = amount_str.split('.')
                cents = cents.ljust(2, '0')  # Ensure cents are two digits
            else:
                dollars = amount_str
                cents = '00'
            amount_cents = int(dollars) * 100 + int(cents)
            if amount_cents > Money.MAX_VALUE:
                raise ValueError(f"Amount exceeds maximum limit: {value}")
            instance = Money(amount_cents)
            if instance.is_valid:
                return instance
            else:
                raise ValueError(f"Invalid money value: {value}")
        else:
            raise ValueError(f"Invalid format for money: {value}")

    @property
    def is_valid(self) -> bool:
        return isinstance(self._value, int) and 0 <= self._value <= Money.MAX_VALUE

    @property
    def value(self) -> int:
        return self._value
