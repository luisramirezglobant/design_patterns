from abc import ABC

class DataBase(ABC):
    def connect(self):
        pass

    def disconnect(self):
        pass

    def execute(self, query):
        pass

class MySQLDataBase(DataBase):
    def connect(self):
        print("Connecting to MySQL database")

    def disconnect(self):
        print("Disconnecting from MySQL database")

    def execute(self, query):
        print(f"Executing query: {query}")

class PostgresDataBase(DataBase):
    def connect(self):
        print("Connecting to Postgres database")

    def disconnect(self):
        print("Disconnecting from Postgres database")

    def execute(self, query):
        print(f"Executing query: {query}")