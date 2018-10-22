from django.urls import path
from .views import ReportViewSet

app_name = 'report'

urlpatterns = [
    path('', ReportViewSet.as_view({'post': 'create'}))
]