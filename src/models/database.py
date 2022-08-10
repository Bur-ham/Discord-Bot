from typing import Dict

from aiosqlite import Connection, Row, connect

from src.utils.schema import PREFIX_CONFIG_SCHEMA

class Database:
    def __init__(self):
        self._connections: Dict[str, Connection] = {}

    async def add_conection(self, name: str, path: str) -> None:
        connection = await connect(path)
        connection.row_factory = Row
        self._connections[name] = connection

    def get_connection(self, __name: str) -> Connection:
        return self._connections[__name]

    async def close_all(self) -> None:
        for i in self._connections.values():
            if i.is_alive():
                await i.close()

    async def commit_all(self) -> None:
        for i in self._connections.values():
            if i.is_alive():
                await i.commit()

    async def initialize_tables(self) -> None:
        config_con = self.get_connection('config')
        async with config_con.cursor() as cursor:
            await cursor.execute(PREFIX_CONFIG_SCHEMA)

    async def __aenter__(self) -> 'Database':
        await self.add_conection('config', './database/config.db')
        await self.initialize_tables()
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.commit_all()
        await self.close_all()

    