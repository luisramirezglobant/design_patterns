class DBSingleton:
    def __init__(self):
        self.write_client = None
        self.read_client = None

    def get_write_engine(self):
        if self.write_client is None:
            raise ValueError(
                "Write DB connection not configured. Please configure write DB connection first."
            )
        return self.write_client

    def get_read_engine(self):
        if self.read_client is None:
            raise ValueError(
                "Read DB connection not configured. Please configure write DB connection first."
            )
        return self.read_client

    async def configure_write_engine(self, connection_string: str) -> None:
        if self.write_client is None:
            self.write_client = await DBFactory.create_write_engine(connection_string)

    async def configure_read_engine(self, connection_string: str) -> None:
        if self.read_client is None:
            self.read_client = await DBFactory.create_read_engine(connection_string)

    def close_connection(self) -> None:
        if self.write_client is not None:
            self.write_client.close()
            self.write_client = None
        if self.read_client is not None:
            self.read_client.close()
            self.read_client = None

db_singleton = DBSingleton()