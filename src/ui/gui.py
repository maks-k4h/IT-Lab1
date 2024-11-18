from pathlib import Path

import gradio as gr
import pandas as pd

from core.service import Service
from core.database import Database
from core.table import Table
from core.parsing.schema import parse_schema
from core.parsing.row import parse_row
from core.filesystem.coder import Coder


class GUI:
    def __init__(self):
        self._service = Service([])
        self._current_database = None
        self._current_table = None

        self._demo = self._build()

    def _build(self) -> gr.Blocks:

        # SET UP UI
        with gr.Blocks() as demo:
            with gr.Row():
                with gr.Column():
                    self._database_selector = self._get_database_selector()

                with gr.Column():
                    self._database_file = gr.File()
                    self._database_import_button = gr.Button(value="Import Database")
                    self._database_export_button = gr.Button(value="Export Database")

                with gr.Column():
                    self._database_name_entry = gr.Textbox(label='Database name')
                    self._create_database_button = gr.Button(value='Create Database')
                    self._delete_database_button = gr.Button(value='Delete Database')

            with gr.Row():
                with gr.Column():
                    self._table_selector = self._get_table_selector()

                with gr.Column():
                    self._table_name_entry = gr.Textbox(label='Table name')
                    self._new_table_schema_entry = gr.TextArea(label='Schema definition', placeholder=(
                        """
                        INT id
                        STRING product_name
                        MONEY product_price
                        """
                    ))
                    self._create_table_button = gr.Button(value='Create Table')
                    self._delete_table_button = gr.Button(value='Delete Database')

            with gr.Column():
                self._table_df = self._get_table_df()
                self._drop_duplicates_button = gr.Button(value='Drop Duplicates')

                with gr.Row():
                    with gr.Column():
                        self._current_schema_text = self._get_current_schema_text()
                        self._new_row_entry = gr.Textbox(label='Row', placeholder='1; Milk; 0.5; $10')
                        self._add_row_button = gr.Button(value='Add Row')
                        self._update_row_button = gr.Button(value='Update Row')

                    with gr.Column():
                        self._delete_row_identifier_entry = gr.Textbox(label='Identifier of the row to be deleted')
                        self._delete_row_button = gr.Button(value='Delete Row')

            # SET UP CALLBACKS
            def _load_page():
                return self._get_database_selector()
            demo.load(
                _load_page,
                outputs=self._database_selector,
            )

            self._create_database_button.click(
                self._create_database,
                inputs=self._database_name_entry,
                outputs=self._database_selector
            )
            self._delete_database_button.click(
                self._delete_database,
                inputs=self._database_name_entry,
                outputs=self._database_selector
            )
            self._database_selector.select(
                self._select_database,
                inputs=self._database_selector,
                outputs=[self._table_selector]
            )
            self._database_import_button.click(
                self._import_database,
                inputs=self._database_file,
                outputs=self._database_selector
            )
            self._database_export_button.click(
                self._export_database,
                outputs=self._database_file,
            )
            self._table_selector.select(
                self._select_table,
                inputs=self._table_selector,
                outputs=[self._table_df, self._current_schema_text]
            )
            self._create_table_button.click(
                self._create_table,
                inputs=[self._table_name_entry, self._new_table_schema_entry],
                outputs=[self._table_selector]
            )
            self._delete_table_button.click(
                self._delete_table,
                inputs=[self._table_name_entry],
                outputs=self._table_selector
            )
            self._add_row_button.click(
                self._add_row,
                inputs=[self._new_row_entry],
                outputs=[self._table_df]
            )
            self._update_row_button.click(
                self._update_row,
                inputs=[self._new_row_entry],
                outputs=[self._table_df]
            )
            self._delete_row_button.click(
                self._delete_row,
                inputs=[self._delete_row_identifier_entry],
                outputs=[self._table_df]
            )
            self._drop_duplicates_button.click(
                self._drop_duplicates,
                outputs=[self._table_df]
            )

        return demo

    def launch(self):
        self._demo.launch()

    def _get_database_selector(self):
        return gr.Dropdown(label='Current database',
                           choices=self._service.databases,)

    def _create_database(self, database_name: str):
        if database_name in self._service.databases:
            raise gr.Error(f"Database {database_name} already exists")
        self._service.add_database(Database(database_name, []))
        return self._get_database_selector()

    def _delete_database(self, database_name: str):
        try:
            self._service.remove_database(database_name)
        except Exception as e:
            raise gr.Error(e)
        return self._get_database_selector()

    def _select_database(self, database_name: str):
        self._current_database = self._service.get_database(database_name)
        return self._get_table_selector()

    def _import_database(self, database_path: str):
        p_db = Path(database_path)
        assert p_db.exists(), "File does not exist"
        self._service.add_database(Coder.import_database(p_db))
        return self._get_database_selector()

    def _export_database(self):
        assert self._current_database is not None, "Select database first"
        p_db = Path(f'{self._current_database.name}.json')
        Coder.export_database(self._current_database, p_db)
        return gr.File(p_db.as_posix())

    def _get_table_selector(self):
        choices = self._current_database.tables if self._current_database else []
        return gr.Dropdown(label='Current table',
                           choices=choices)

    def _select_table(self, table_name: str):
        self._current_table = self._current_database.get_table(table_name)
        return self._get_table_df(), self._get_current_schema_text()

    def _create_table(self, table_name: str, schema_definition: str):
        try:
            schema = parse_schema(schema_definition)
            table = Table(name=table_name, sch=schema, rows=[])
            self._current_database.add_table(table)
        except Exception as e:
            raise gr.Error(e)
        return self._get_table_selector()

    def _delete_table(self, table_name: str):
        try:
            self._current_database.remove_table(table_name)
        except Exception as e:
            raise gr.Error(e)
        return self._get_table_selector()

    def _get_table_df(self):
        df = self._current_table.to_df() if self._current_table else None
        return gr.Dataframe(df) if df is not None else gr.Dataframe()

    def _add_row(self, row_str: str):
        assert self._current_table is not None, "Select the table first"
        row = parse_row(self._current_table.schema, row_str)
        self._current_table.insert(row)
        return self._get_table_df()

    def _update_row(self, row_str: str):
        assert self._current_table is not None, "Select the table first"
        row = parse_row(self._current_table.schema, row_str)
        self._current_table.update(row)
        return self._get_table_df()

    def _delete_row(self, row_id: str):
        assert self._current_table is not None, "Select the table first"
        identifier = self._current_table.schema.id_type.from_string(row_id)
        self._current_table.delete(identifier)
        return self._get_table_df()

    def _get_current_schema_text(self):
        if self._current_table is None:
            return gr.Dataframe()
        df = pd.DataFrame(columns=['Type', 'Name'], data=[
            (self._current_table.schema.id_type_name.value, 'id'),
            *[(t.value, n) for t, n in zip(self._current_table.schema.type_names, self._current_table.schema.column_names)]
        ])
        return gr.Dataframe(df)

    def _drop_duplicates(self):
        assert self._current_table is not None, "Select the table first"
        self._current_table.drop_duplicates()
        return self._get_table_df()
