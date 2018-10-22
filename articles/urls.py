from django.urls import path

from .views import *

app_name = 'article'

urlpatterns = [
    path('', NoticeViewSet.as_view({'get':'list'})),
    path('<slug>/', NoticeViewSet.as_view({'get':'retrieve'}))
]