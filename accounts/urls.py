from django.urls import path, include

from .views import UserViewSet, UserMeViewSet
app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', UserViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('me/', UserMeViewSet.as_view({'get':'me'})),
    path('me/soundcloud-token/', UserMeViewSet.as_view({'get': 'get_soundcloud_token'}))
]