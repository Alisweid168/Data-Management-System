# Data Management System

## Overview
This project is a backend Data Management System built with Django 5 and PostgreSQL 16. It provides dynamic schema management, CRUD operations, large-scale data import with validation, and secure APIs with JWT authentication. Asynchronous processing is handled via Celery, and email notifications are sent upon import completion.

## Features
- **Schema Management**
  - Create, update, and delete tables dynamically.
  - Modify table schemas by adding or removing fields.
- **CRUD Operations**
  - Standard Create, Read, Update, and Delete operations.
  - Search functionality with filtering and sorting.
  - Pagination support for large datasets.
- **Data Import**
  - Import large CSV files (100,000+ records) asynchronously.
  - Validate data against defined schemas.
  - Error handling and reporting for invalid data.
- **Email Notifications**
  - Send confirmation emails upon successful data import.
- **Security**
  - Secure API endpoints with JWT authentication.
- **Tech Stack**
  - Python 3.12
  - Django 5
  - PostgreSQL 16
  - Celery (for asynchronous processing)
  - Redis (as Celery broker)
  - JWT Authentication (via Django REST Framework Simple JWT)

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.12
- PostgreSQL 16
- Redis (for Celery)
- Virtual Environment (recommended)

### Setup Instructions
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/Alisweid168/Data-Management-System.git
   cd data-management-system
   ```
2. **Create and Activate a Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply Migrations and Create Superuser:**
   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Run the Server:**
   ```sh
   python manage.py runserver
   ```
6. **Start Celery Worker:**
   ```sh
   celery -A project_name worker --loglevel=info
   ```

## API Endpoints

### Schema Management
- `POST /schemas/create_table/` - Create a new table
-   - **Content-Type:** `application/json`
  - **Request Body:**
    ```json
    {
      "table_name": "customer",
      "fields": {
        "name": "text",
        "email": "text unique",
        "created_at": "date"
      }
    }
    ```
- `POST /schemas/add_column/` - Update table schema
-   - **Content-Type:** `application/json`
  - **Request Body:**
    ```json
      {
      "table_name": "customer",
      "column_name": "age",
      "column_type": "INTEGER"
      }

    ```
- `DELETE /schemas/delete_table/` - Delete a table
-   - **Request Body:**
    ```json
      {
      "table_name": "customer",
      }
    ```
### CRUD Operations
- `POST /crud/create_record/` - Create a record
- **Content-Type:** `application/json`
  - **Request Body:**
    ```json
    {
      "table_name": "Customer",
      "data": {
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
    ```
- `GET /crud/read_records/` - Retrieve records (supports filtering, sorting, pagination)
- - **Parameters:**
    - `table_name` (string, required) - Name of the table
    - `filters` (JSON, optional) - Filtering conditions
    - `search` (JSON, optional) - Search criteria
    - `sort_by` (string, optional) - Field to sort by
    - `order` (string, optional) - `asc` or `desc`
    - `limit` (integer, optional) - Number of records per page
    - `offset` (integer, optional) - Starting record index
  
- `PUT /crud/update_record/` - Update a record
-   - **Content-Type:** `application/json`
  - **Request Body:**
    ```json
    {
      "table_name": "Customer",
      "id": 1,
      "data": {
        "name": "Jane Doe"
      }
    }
    ```
- `DELETE /crud/delete_record/` - Delete a record
- **Content-Type:** `application/json`
  - **Request Body:**
    ```json
   {
      "table_name": "customer3",
      "id": 1
   }
    ```

### Data Import
- `POST /import/upload/` - Upload and import a CSV file
-  - **Content-Type:** `multipart/form-data`
  - **Request Body:**
    - `file` (CSV file, required) - The CSV file containing data

### Authentication
- `POST /api/token/` - Get JWT token
- **Content-Type:** `application/json`
  - **Request Body:**
    ```json
    {
      "username": "ali",
      "password": "ali123456789"
    }
    ```
- `POST /api/token/refresh/` - Refresh JWT token
  - **Content-Type:** `application/json`
  - **Request Body:**
    ```json
    {
      "username": "ali",
      "password": "ali123456789",
      "refresh": "..."
    }
    ```
