from typing import List

from .row import Row
from . import schema, datatypes


class Table:
    def __init__(self, sch: schema.TableSchema, rows: List[Row]):
        self._schema = sch
        self._rows = rows

    @property
    def schema(self) -> schema.TableSchema:
        return self._schema

    @property
    def rows(self) -> List[Row]:
        return self._rows

    def validate(self) -> bool:
        # validate rows
        for row in self._rows:
            if not self.validate_row(row):
                return False
        # validate uniqueness of identifiers
        identifiers = [row.identifier for row in self._rows]
        if len(identifiers) != len(set(identifiers)):
            return False
        return True

    def validate_row(self, row: Row) -> bool:
        # validate values
        if not row.validate():
            return False
        # validate schema
        if not type(row.identifier) is self._schema.id_type:
            return False
        for v, d_type in zip(row.values, self._schema.types):
            if not type(v) is d_type:
                return False

    def insert(self, row: Row) -> None:
        assert row.identifier not in {r.identifier for r in self._rows}
        assert self.validate_row(row)
        self._rows.append(row)

    def update(self, row: Row) -> None:
        assert self.validate_row(row)
        for i in range(len(self._rows)):
            if self._rows[i].identifier == row.identifier:
                self._rows[i] = row
                return
        raise ValueError(f"Cannot update row {row.identifier} — not found")

    def delete(self, identifier: datatypes.DataType) -> None:
        assert type(identifier) is self._schema.id_type
        index = None
        for i, row in enumerate(self._rows):
            if row.identifier == identifier:
                index = i
                break
        assert index is not None, f"Cannot delete row {identifier} — not found"
        del self._rows[index]

