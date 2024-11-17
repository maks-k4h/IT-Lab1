from .data_type import DataType


class Char(DataType):
    def __init__(self, value: str):
        if len(value) != 1:
            raise ValueError("Char must be a single character.")
        self._value = value

    def __str__(self) -> str:
        return self._value

    @staticmethod
    def from_string(value: str) -> 'Char':
        if len(value) != 1:
            raise ValueError("Char must be a single character.")
        instance = Char(value)
        if instance.is_valid:
            return instance
        else:
            raise ValueError(f"Invalid char value: {value}")

    @property
    def is_valid(self) -> bool:
        return isinstance(self._value, str) and len(self._value) == 1

    @property
    def value(self) -> str:
        return self._value
