from django.urls import path
from .views import CreateRecordView, ReadRecordsView, UpdateRecordView, DeleteRecordView
    
    
urlpatterns = [
    path("create_record/", CreateRecordView.as_view(), name="create_record"),
    path("read_records/", ReadRecordsView.as_view(), name="read_records"),
    path("update_record/", UpdateRecordView.as_view(), name="update_record"),
    path("delete_record/", DeleteRecordView.as_view(), name="delete_record"),

]