from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
application = get_wsgi_application()

class SchemaManagementTests(APITestCase):
    BASE_URL = "http://127.0.0.1:8000/schemas/"
    AUTH_URL = "http://127.0.0.1:8000/auth/token/"
    TEST_CREDENTIALS = {"username": "alisweidan", "password": "ali12345678"}

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_auth_token()}")

    def get_auth_token(self):
        """Helper function to obtain auth token."""
        response = self.client.post(self.AUTH_URL, self.TEST_CREDENTIALS, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def _post(self, endpoint, data):
        return self.client.post(f"{self.BASE_URL}{endpoint}/", data, format="json")

    def _delete(self, endpoint, data):
        return self.client.delete(f"{self.BASE_URL}{endpoint}/", data, format="json")

    @patch("schemas.views.schema_manager.create_table")
    def test_create_table_success(self, mock_create_table):
        """Test creating a table successfully"""
        data = {
            "table_name": "Customer",
            "fields": {"name": "TEXT", "email": "TEXT UNIQUE", "created_at": "DATE"}
        }
        response = self._post("create_table", data)
        
        if response.status_code == status.HTTP_201_CREATED:
            print("✅ test_create_table_success PASSED")
        else:
            print("❌ test_create_table_success FAILED")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Table 'Customer' created successfully.")
        mock_create_table.assert_called_once_with("Customer", data["fields"])

    @patch("schemas.views.schema_manager.create_table")
    def test_create_table_missing_fields(self, mock_create_table):
        """Test creating a table with missing fields"""
        response = self._post("create_table", {"table_name": "Customer"})
        
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("✅ test_create_table_missing_fields PASSED")
        else:
            print("❌ test_create_table_missing_fields FAILED")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Table name and fields are required.")

    @patch("schemas.views.schema_manager.add_column")
    def test_add_column_success(self, mock_add_column):
        """Test adding a column successfully"""
        data = {"table_name": "Customer", "column_name": "phone_number", "column_type": "TEXT"}
        response = self._post("add_column", data)
        
        if response.status_code == status.HTTP_200_OK:
            print("✅ test_add_column_success PASSED")
        else:
            print("❌ test_add_column_success FAILED")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Column 'phone_number' added to 'Customer'.")
        mock_add_column.assert_called_once_with("Customer", "phone_number", "TEXT")

    @patch("schemas.views.schema_manager.add_column")
    def test_add_column_missing_fields(self, mock_add_column):
        """Test adding a column with missing fields"""
        response = self._post("add_column", {"table_name": "Customer"})
        
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("✅ test_add_column_missing_fields PASSED")
        else:
            print("❌ test_add_column_missing_fields FAILED")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Table name, column name, and column type are required.")

    @patch("schemas.views.schema_manager.delete_table")
    def test_delete_table_success(self, mock_delete_table):
        """Test deleting a table successfully"""
        response = self._delete("delete_table", {"table_name": "Customer"})
        
        if response.status_code == status.HTTP_200_OK:
            print("✅ test_delete_table_success PASSED")
        else:
            print("❌ test_delete_table_success FAILED")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Table 'Customer' deleted successfully.")
        mock_delete_table.assert_called_once_with("Customer")

    @patch("schemas.views.schema_manager.delete_table")
    def test_delete_table_missing_name(self, mock_delete_table):
        """Test deleting a table with missing name"""
        response = self._delete("delete_table", {})
        
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("✅ test_delete_table_missing_name PASSED")
        else:
            print("❌ test_delete_table_missing_name FAILED")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Table name is required.")
    
    # def tearDown(self):
    #     """Clean up after each test by closing the database connection."""
    #     connection.close()