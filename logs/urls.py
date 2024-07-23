from django.urls import path
from .views import SetFolderView, DownloadLogView

urlpatterns = [
    path('set_folder/', SetFolderView.as_view(), name='set_folder'),
    path('download_log/', DownloadLogView.as_view(), name='download_log'),
]