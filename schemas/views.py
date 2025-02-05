from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .schema_manager import SchemaManager

schema_manager = SchemaManager()

class CreateTableView(APIView):
    def post(self, request):
        table_name = request.data.get("table_name")
        fields = request.data.get("fields")  # Example: {"name": "TEXT", "email": "TEXT UNIQUE", "created_at": "DATE"}

        if not table_name or not fields:
            return Response({"error": "Table name and fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        schema_manager.create_table(table_name, fields)
        return Response({"message": f"Table '{table_name}' created successfully."}, status=status.HTTP_201_CREATED)

class AddColumnView(APIView):
    def post(self, request):
        table_name = request.data.get("table_name")
        column_name = request.data.get("column_name")
        column_type = request.data.get("column_type")

        if not table_name or not column_name or not column_type:
            return Response({"error": "Table name, column name, and column type are required."}, status=status.HTTP_400_BAD_REQUEST)

        schema_manager.add_column(table_name, column_name, column_type)
        return Response({"message": f"Column '{column_name}' added to '{table_name}'."}, status=status.HTTP_200_OK)

class DeleteTableView(APIView):
    def delete(self, request):
        table_name = request.data.get("table_name")

        if not table_name:
            return Response({"error": "Table name is required."}, status=status.HTTP_400_BAD_REQUEST)

        schema_manager.delete_table(table_name)
        return Response({"message": f"Table '{table_name}' deleted successfully."}, status=status.HTTP_200_OK)
