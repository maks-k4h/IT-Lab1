from .data_type import DataType


class Integer(DataType):
    def __init__(self, value: int):
        self._value = value

    def __str__(self) -> str:
        return str(self._value)

    @staticmethod
    def from_string(value: str) -> 'Integer':
        try:
            new_value = int(value)
            instance = Integer(new_value)
            if instance.is_valid:
                return instance
            else:
                raise ValueError(f"Invalid integer value: {value}")
        except ValueError:
            raise ValueError(f"Invalid integer value: {value}")

    @property
    def is_valid(self) -> bool:
        return isinstance(self._value, int)

    @property
    def value(self) -> str:
        return str(self._value)
