from typing import List, Union

import pandas as pd

from .row import Row
from . import schema, datatypes


class Table:
    def __init__(self, name: str, sch: schema.TableSchema, rows: List[Row]):
        self._name = name
        self._schema = sch
        self._rows = rows

    @property
    def name(self) -> str:
        return self._name

    @property
    def schema(self) -> schema.TableSchema:
        return self._schema

    def to_df(self) -> pd.DataFrame:
        data = [(r.identifier, *(v.value for v in r.values)) for r in self._rows]
        df = pd.DataFrame(
            data=data,
            columns=['id', *self.schema.column_names],
        )
        return df

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
        return True

    def insert(self, row: Row) -> None:
        assert row.identifier.value not in {r.identifier.value for r in self._rows}
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
        assert type(identifier) is self._schema.id_type, (type(identifier), self._schema.id_type)
        index = None
        for i, row in enumerate(self._rows):
            if row.identifier.value == identifier.value:
                index = i
                break
        assert index is not None, f"Cannot delete row {identifier} — not found"
        del self._rows[index]
