from django.urls import path

from .views import TrackViewSet, TrackCommentViewSet, TrackCommentDetailViewSet, TrackLikeViewSet

app_name = 'track'

urlpatterns = [
    path('', TrackViewSet.as_view({'get':'list', 'post': 'create'})),
    path('<int:track_id>/', TrackViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('<int:track>/comments/', TrackCommentViewSet.as_view({'get':'list', 'post': 'create'})),
    path('<int:track>/comments/<int:pk>/', TrackCommentDetailViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('<int:track>/like/', TrackLikeViewSet.as_view({'post':'create'})),
]