from abc import ABC
from dataclasses import dataclass

from database import DataBase

@dataclass
class ORM(ABC):
    database: DataBase

    def save(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

class UserORM(ORM):
    def save(self):
        self.database.connect()
        self.database.execute("INSERT INTO users VALUES (1, 'John Doe')")
        self.database.disconnect()

    def delete(self):
        self.database.connect()
        self.database.execute("DELETE FROM users WHERE id = 1")
        self.database.disconnect()

    def update(self):
        self.database.connect()
        self.database.execute("UPDATE users SET name = 'Jane Doe' WHERE id = 1")
        self.database.disconnect()

class ProductORM(ORM):
    def save(self):
        self.database.connect()
        self.database.execute("INSERT INTO products VALUES (1, 'Laptop')")
        self.database.disconnect()

    def delete(self):
        self.database.connect()
        self.database.execute("DELETE FROM products WHERE id = 1")
        self.database.disconnect()

    def update(self):
        self.database.connect()
        self.database.execute("UPDATE products SET name = 'Desktop' WHERE id = 1")
        self.database.disconnect()

    def read(self):
        self.database.connect()
        self.database.execute("SELECT * FROM products")
        self.database.disconnect()