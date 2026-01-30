from django.urls import path
from .views import UploadCSVView, DatasetSummaryView, DatasetRawDataView

# API endpoints for datasets
urlpatterns = [
    path('upload-csv/', UploadCSVView.as_view(), name='upload-csv'),
    path('dataset/<int:id>/summary/', DatasetSummaryView.as_view(), name='dataset-summary'),
    path('dataset/<int:id>/data/', DatasetRawDataView.as_view(), name='dataset-raw-data'),
]
