from .data_type import DataType


class String(DataType):
    def __init__(self, value: str):
        self._value = value

    def __str__(self) -> str:
        return self._value

    @staticmethod
    def from_string(value: str) -> 'String':
        instance = String(value)
        if instance.is_valid:
            return instance
        else:
            raise ValueError(f"Invalid string value: {value}")

    @property
    def is_valid(self) -> bool:
        return isinstance(self._value, str)

    @property
    def value(self) -> str:
        return self._value
