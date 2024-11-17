from core.schema import TableSchema
from core.row import Row


def parse_row(schema: TableSchema, definition: str) -> Row:
    str_values = definition.split(';')
    identifier = schema.id_type.from_string(str_values[0])
    values = []
    for str_v, v_type in zip(str_values[1:], schema.types):
        values.append(v_type.from_string(str_v.strip()))

    return Row(identifier, values)
