from typing import List, Union

from .table import Table


class Database:

    def __init__(self, name: str, tables: List[Table]) -> None:
        self._name = name
        self._tables = tables

    @property
    def name(self) -> str:
        return self._name

    @property
    def tables(self) -> List[str]:
        return [t.name for t in self._tables]

    def get_table(self, name: str) -> Union[Table, None]:
        tables = [t for t in self._tables if t.name == name]
        if len(tables) == 0:
            return None
        return tables[0]

    def add_table(self, table: Table) -> None:
        assert table.name not in [t.name for t in self._tables], 'Table name must be unique'
        self._tables.append(table)

    def remove_table(self, table_name) -> None:
        for i in range(len(self._tables)):
            if self._tables[i].name == table_name:
                del self._tables[i]
                return
        raise ValueError(f'Table {table_name} is not in the database')
