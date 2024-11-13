from data_type import DataType


class Real(DataType):
    def __init__(self, value: float):
        self._value = value

    def __str__(self) -> str:
        return str(self._value)

    @staticmethod
    def from_string(value: str) -> 'Real':
        try:
            new_value = float(value)
            instance = Real(new_value)
            if instance.is_valid:
                return instance
            else:
                raise ValueError(f"Invalid real number value: {value}")
        except ValueError:
            raise ValueError(f"Invalid real number value: {value}")

    @property
    def is_valid(self) -> bool:
        return isinstance(self._value, float)

    @property
    def value(self) -> float:
        return self._value
