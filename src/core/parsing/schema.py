from core.schema import TableSchema, TypeNames


def parse_schema(table_schema: str) -> TableSchema:
    id_col_type = None
    col_names = []
    col_types = []
    for line in table_schema.strip().splitlines():
        type_name, col_name, *other = line.split()
        assert len(other) == 0
        col_type = TypeNames(type_name.lower())
        if col_name.lower() == 'id':
            id_col_type = col_type
        else:
            col_names.append(col_name)
            col_types.append(col_type)
    assert id_col_type is not None, 'id column is not defined!'

    return TableSchema(id_type_name=id_col_type, col_names=col_names, type_names=col_types)

