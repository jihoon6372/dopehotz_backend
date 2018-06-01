from django.urls import path, include

from .views import UserViewSet
app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', UserViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('me/', UserViewSet.as_view({'get':'me'}))
]