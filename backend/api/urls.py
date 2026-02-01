from django.urls import path
from .views import UploadCSVView, DatasetSummaryView, DatasetRawDataView, DatasetPDFView, DatasetListView, SignupView, LoginView

# API endpoints for datasets
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload-csv/', UploadCSVView.as_view(), name='upload-csv'),
    path('datasets/', DatasetListView.as_view(), name='dataset-list'),
    path('dataset/<int:id>/summary/', DatasetSummaryView.as_view(), name='dataset-summary'),
    path('dataset/<int:id>/data/', DatasetRawDataView.as_view(), name='dataset-raw-data'),
    path('dataset/<int:id>/pdf/', DatasetPDFView.as_view(), name='dataset-pdf'),
]
