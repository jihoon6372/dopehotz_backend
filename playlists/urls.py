from django.urls import path

from .views import PlayListGroupViewSet, test, PlayListUpdateViewSet

app_name = 'track'

urlpatterns = [
    path('group/', PlayListGroupViewSet.as_view({'get':'list', 'post': 'create'})),
    path('group/<int:pk>/', PlayListGroupViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('group/<int:pk>/change/', PlayListUpdateViewSet.as_view({'put':'update'})),
    path('test/', test),
]