import psycopg2
from django.conf import settings

class CRUDManager:
    def __init__(self):
        """Initialize database connection"""
        self.conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_record(self, table_name, data):
        """Insert a new record into a table."""
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING id;"
        self.cursor.execute(query, list(data.values()))
        return self.cursor.fetchone()[0]

    def read_records(self, table_name, filters=None, search=None, sort_by=None, order="asc", limit=10, offset=0):
        """Read records with filtering, search, sorting, and pagination."""
        query = f"SELECT * FROM {table_name}"
        conditions = []
        values = []

        # Apply filtering
        if filters:
            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                values.append(value)

        # Apply search
        if search:
            search_conditions = [f"{key} ILIKE %s" for key in search.keys()]
            conditions.append(f"({' OR '.join(search_conditions)})")
            values.extend([f"%{value}%" for value in search.values()])

        # Append conditions
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Apply sorting
        if sort_by:
            query += f" ORDER BY {sort_by} {order.upper()}"

        # Apply pagination
        query += " LIMIT %s OFFSET %s"
        values.extend([limit, offset])

        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def update_record(self, table_name, record_id, data):
        """Update an existing record."""
        # Check if record exists
        self.cursor.execute(f"SELECT id FROM {table_name} WHERE id = %s;", [record_id])
        if not self.cursor.fetchone():
            return None  # No record found

        # Build the update query
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s RETURNING id;"
        
        # Debugging logs
        print("Executing query:", query, "with values:", list(data.values()) + [record_id])

        self.cursor.execute(query, list(data.values()) + [record_id])
        updated_record = self.cursor.fetchone()
        
        self.conn.commit()  # Ensure changes are saved

        return updated_record[0] if updated_record else None 
    
    def delete_record(self, table_name, record_id):
        """Delete a record."""
        query = f"DELETE FROM {table_name} WHERE id = %s RETURNING id;"
        self.cursor.execute(query, [record_id])
        return self.cursor.fetchone()
