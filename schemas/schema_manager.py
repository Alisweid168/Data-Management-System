import psycopg2
from django.conf import settings

class SchemaManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, fields):
        """
        Creates a new table dynamically with an auto-incrementing primary key (id).
        Example: create_table("Customer", {"name": "TEXT", "email": "TEXT UNIQUE", "created_at": "DATE"})
        """
        # Add 'id' column with auto-increment (SERIAL) and PRIMARY KEY
        field_definitions = ", ".join([f"{name} {dtype}" for name, dtype in fields.items()])
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,  -- Auto-incrementing ID
                {field_definitions}
            );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_column(self, table_name, column_name, column_type):
        """
        Adds a new column to an existing table.
        Example: add_column("Customer", "phone_number", "TEXT")
        """
        query = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type};"
        self.cursor.execute(query)

    def delete_table(self, table_name):
        """
        Deletes a table.
        Example: delete_table("Customer")
        """
        query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        self.cursor.execute(query)
