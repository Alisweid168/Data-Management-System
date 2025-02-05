from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .crud_manager import CRUDManager
import json

crud_manager = CRUDManager()

class CreateRecordView(APIView):
    def post(self, request):
        table_name = request.data.get("table_name")
        data = request.data.get("data")

        if not table_name or not isinstance(data, dict):
            return Response({"error": "Valid table name and data dictionary are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record_id = crud_manager.create_record(table_name, data)
            return Response({"message": "Record created", "id": record_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReadRecordsView(APIView):
    def get(self, request):
        table_name = request.query_params.get("table_name")
        filters = request.query_params.get("filters", "{}")
        search = request.query_params.get("search", "{}")
        sort_by = request.query_params.get("sort_by")
        order = request.query_params.get("order", "asc").lower()
        limit = request.query_params.get("limit", "10")
        offset = request.query_params.get("offset", "0")

        # Ensure table name is provided
        if not table_name:
            return Response({"error": "Table name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert string parameters to proper data types
        try:
            filters = json.loads(filters)  # Convert JSON string to dict
            search = json.loads(search)  # Convert JSON string to dict

            # Define allowed fields (excluding 'id')
            allowed_filters = {"name", "email", "created_at"}
            allowed_search_fields = {"name", "email", "created_at"}

            # Remove 'id' from filters and search
            filters = {k: v for k, v in filters.items() if k in allowed_filters}
            search = {k: v for k, v in search.items() if k in allowed_search_fields}

            # Convert date fields correctly
            if "created_at" in filters:
                filters["created_at"] = str(filters["created_at"])  

            # Validate `sort_by` to prevent SQL injection
            allowed_sort_fields = ["name", "email", "created_at"]
            if sort_by and sort_by not in allowed_sort_fields:
                return Response({"error": f"Invalid sort_by field: {sort_by}"}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure valid order
            if order not in ["asc", "desc"]:
                return Response({"error": "Order must be 'asc' or 'desc'."}, status=status.HTTP_400_BAD_REQUEST)

            limit = max(1, int(limit))
            offset = max(0, int(offset))

        except (ValueError, TypeError, json.JSONDecodeError):
            return Response({"error": "Invalid input format."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch records from the database
        try:
            records = crud_manager.read_records(table_name, filters, search, sort_by, order, limit, offset)
            return Response({"records": records}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateRecordView(APIView):
    def put(self, request):
        table_name = request.data.get("table_name")
        record_id = request.data.get("id")
        data = request.data.get("data")

        if not table_name or not record_id or not data:
            return Response({"error": "Table name, ID, and data are required."}, status=status.HTTP_400_BAD_REQUEST)

        updated = crud_manager.update_record(table_name, record_id, data)
        return Response({"message": "Record updated", "id": updated}, status=status.HTTP_200_OK)

class DeleteRecordView(APIView):
    def delete(self, request):
        table_name = request.data.get("table_name")
        record_id = request.data.get("id")

        if not table_name or not record_id:
            return Response({"error": "Table name and ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        deleted = crud_manager.delete_record(table_name, record_id)
        return Response({"message": "Record deleted", "id": deleted}, status=status.HTTP_200_OK)
