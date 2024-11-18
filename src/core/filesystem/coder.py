import json
from pathlib import Path
from typing import List, Dict

from core.row import Row
from core.table import Table
from core.database import Database
from core.schema import TableSchema, TypeNames


class Coder:
    @staticmethod
    def export_database(db: Database, path: Path) -> None:
        path.write_text(Coder.database_to_json(db))

    @staticmethod
    def import_database(path: Path) -> Database:
        return Coder.json_to_database(path.read_text())

    @staticmethod
    def database_to_json(db: Database) -> str:
        data = {
            'name': db.name,
            'tables': []
        }
        for table_name in db.tables:
            data['tables'].append(Coder.table_to_dict(db.get_table(table_name)))
        return json.dumps(data, indent=2)

    @staticmethod
    def json_to_database(json_data: str) -> Database:
        data = json.loads(json_data)
        tables = []
        for table_data in data['tables']:
            tables.append(Coder.dict_to_table(table_data))
        return Database(data['name'], tables=tables)

    @staticmethod
    def table_to_dict(table: Table) -> Dict:
        return {
            'name': table.name,
            'schema': Coder._schema_to_list(table.schema),
            'rows': [(row.identifier.value, *[v.value for v in row.values]) for row in table.rows],
        }

    @staticmethod
    def dict_to_table(data: Dict) -> Table:
        name = data['name']
        schema = Coder._list_to_schema(data['schema'])
        rows = []
        for row_data in data['rows']:
            identifier = schema.id_type.from_string(row_data[0])
            values = []
            for t, s in zip(schema.types, row_data[1:]):
                values.append(t.from_string(str(s)))
            rows.append(Row(identifier, values))
        return Table(name, schema, rows)

    @staticmethod
    def _schema_to_list(schema: TableSchema) -> List:
        column_defs = [(schema.id_type_name.value, 'id')]
        for tn, cn in zip(schema.type_names, schema.column_names):
            column_defs.append((tn.value, cn))
        return column_defs

    @staticmethod
    def _list_to_schema(lst: List) -> TableSchema:
        id_type = None
        column_types = []
        column_names = []
        for tn, cn in lst:
            if cn == 'id':
                id_type = TypeNames(tn)
            else:
                column_names.append(cn)
                column_types.append(TypeNames(tn))
        return TableSchema(col_names=column_names, type_names=column_types, id_type_name=id_type)
