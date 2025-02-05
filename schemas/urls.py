from django.urls import path
from .views import CreateTableView, AddColumnView, DeleteTableView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("create_table/", CreateTableView.as_view(), name="create_table"),
    path("add_column/", AddColumnView.as_view(), name="add_column"),
    path("delete_table/", DeleteTableView.as_view(), name="delete_table"),

]