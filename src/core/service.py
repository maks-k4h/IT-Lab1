from typing import List, Union

from .database import Database


class Service:
    def __init__(self, databases: List[Database]):
        self._databases = databases

    def get_database(self, database_name: str) -> Union[Database, None]:
        for database in self._databases:
            if database.name == database_name:
                return database
        return None

    def add_database(self, database: Database):
        assert not self.get_database(database.name), "Database already exists"
        self._databases.append(database)

    def remove_database(self, database_name: str):
        for i in range(len(self._databases)):
            if self._databases[i].name == database_name:
                del self._databases[i]
        raise ValueError('Database does not exist')

    @property
    def databases(self) -> List[str]:
        return [d.name for d in self._databases]
