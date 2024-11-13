from typing import List, Any

from . import datatypes


class Row:
    def __init__(self, identifier: datatypes.DataType, values: List[datatypes.DataType]):
        self._identifier = identifier
        self._values = values

    @property
    def identifier(self) -> datatypes.DataType:
        return self._identifier

    @property
    def values(self) -> List[datatypes.DataType]:
        return self._values

    def __str__(self) -> str:
        return ', '.join(str(value) for value in self.values)

    def validate(self) -> bool:
        return all(value.is_valid for value in self.values) and self.identifier.is_valid
