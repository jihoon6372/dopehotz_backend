from django.urls import path

from .views import *

urlpatterns = [
    path('log/', DiscordLogView.as_view({'get':'list', 'post': 'create'})),
]