from pathlib import Path

from fastapi import APIRouter, HTTPException, Response, UploadFile, responses, Body

from api.models import service
from http import HTTPStatus

from core import database, parsing
from core.filesystem import coder


router = APIRouter(prefix="/databases", tags=[])


@router.get("/", tags=['databases'])
async def get_all_databases():
    return service.databases


@router.post("/create", tags=['databases'])
async def create_database(database_name: str):
    if database_name in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database already exists')
    db = database.Database(database_name, [])
    service.add_database(db)
    return Response(status_code=HTTPStatus.CREATED)


@router.delete("/{database_name}", tags=['databases'])
async def delete_database(database_name: str):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    service.remove_database(database_name)
    return Response(status_code=HTTPStatus.OK)


@router.get("/{database_name}/export", tags=['databases'])
async def export_database(database_name: str):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    p_exports = Path('_exports/')
    p_exports.mkdir(exist_ok=True)
    coder.Coder().export_database(service.get_database(database_name), p_exports / f'{database_name}.json')
    return responses.FileResponse(p_exports / f'{database_name}.json')


@router.post("/import", tags=['databases'])
async def import_database(db_file: UploadFile):
    db = coder.Coder.json_to_database((await db_file.read()).decode())
    if db.name in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database already exists')
    service.add_database(db)
    return Response(status_code=HTTPStatus.CREATED)


@router.get("/{database_name}", tags=['tables'])
def list_tables(database_name: str):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    return service.get_database(database_name).tables


@router.delete('/{database_name}/{table_name}', tags=['tables'])
async def delete_table(database_name: str, table_name: str):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    db = service.get_database(database_name)
    if table_name not in db.tables:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Table does not exist')
    db.remove_table(table_name)
    return Response(status_code=HTTPStatus.OK)


@router.post("/{database_name}/create", tags=['tables'])
def create_table(database_name: str, table_name: str, table_schema: str = Body(..., media_type='text/plain')):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    db = service.get_database(database_name)
    if table_name in db.tables:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Table already exists')
    schema = parsing.schema.parse_schema(table_schema)
    table = database.Table(table_name, schema, [])
    db.add_table(table)
    return Response(status_code=HTTPStatus.CREATED)


@router.post("{database_name}/{table_name}/drop-duplicates", tags=['tables'])
def drop_duplicates(database_name: str, table_name: str):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    db = service.get_database(database_name)
    if table_name not in db.tables:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Table does not exist')
    table = db.get_table(table_name)
    table.drop_duplicates()
    return Response(status_code=HTTPStatus.OK)


@router.get("/{database_name}/{table_name}", tags=['rows'])
def list_rows(database_name: str, table_name: str):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    db = service.get_database(database_name)
    if table_name not in db.tables:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Table does not exist')
    table = db.get_table(table_name)
    return [str(r) for r in table.rows]


@router.post("/{database_name}/{table_name}", tags=['rows'])
def insert_row(database_name: str, table_name: str, row_data: str = Body(..., media_type='text/plain')):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    db = service.get_database(database_name)
    if table_name not in db.tables:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Table does not exist')
    table = db.get_table(table_name)
    row = parsing.row.parse_row(table.schema, row_data)
    table.insert(row)
    return Response(status_code=HTTPStatus.OK)


@router.put("/{database_name}/{table_name}", tags=['rows'])
def update_row(database_name: str, table_name: str, row_data: str = Body(..., media_type='text/plain')):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    db = service.get_database(database_name)
    if table_name not in db.tables:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Table does not exist')
    table = db.get_table(table_name)
    row = parsing.row.parse_row(table.schema, row_data)
    table.update(row)
    return Response(status_code=HTTPStatus.OK)


@router.delete("/{database_name}/{table_name}/{row_id}", tags=['rows'])
def delete_row(database_name: str, table_name: str, row_id: int):
    if database_name not in service.databases:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Database does not exist')
    db = service.get_database(database_name)
    if table_name not in db.tables:
        raise HTTPException(HTTPStatus.BAD_REQUEST, 'Table does not exist')
    table = db.get_table(table_name)
    table.delete(row_id)
    return Response(status_code=HTTPStatus.OK)


