import re

from .data_type import DataType
from .money import Money


class MoneyInterval(DataType):
    def __init__(self, lower: Money, upper: Money):
        if lower.value > upper.value:
            raise ValueError("Lower bound must be less than or equal to upper bound.")
        self._lower = lower
        self._upper = upper

    def __str__(self) -> str:
        return f"{self._lower} - {self._upper}"

    @staticmethod
    def from_string(value: str) -> 'MoneyInterval':
        pattern = r'^\$\d+(\.\d{2})?-\$\d+(\.\d{2})?$'
        if re.match(pattern, value):
            lower_str, upper_str = value.split('-')
            lower = Money.from_string(lower_str)
            upper = Money.from_string(upper_str)
            instance = MoneyInterval(lower, upper)
            if instance.is_valid:
                return instance
            else:
                raise ValueError(f"Invalid money interval value: {value}")
        else:
            raise ValueError(f"Invalid format for money interval: {value}")

    @property
    def is_valid(self) -> bool:
        return self._lower.is_valid and self._upper.is_valid and self._lower.value <= self._upper.value

    @property
    def value(self) -> tuple:
        return self._lower.value, self._upper.value
