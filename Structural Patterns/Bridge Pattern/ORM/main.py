from database import MySQLDataBase, PostgresDataBase
from ORM import UserORM, ProductORM

def main():
    # Create a MySQL database and an ORM
    mysql_database = MySQLDataBase()
    user_orm = UserORM(mysql_database)

    # Save, delete, and update a user
    user_orm.save()
    user_orm.update()
    user_orm.delete()

    # Create a Postgres database and an ORM
    postgres_database = PostgresDataBase()
    product_orm = ProductORM(postgres_database)

    # Save, delete, and update a product
    product_orm.save()
    product_orm.update()
    product_orm.read()
    product_orm.delete()

if __name__ == "__main__":
    main()