from django.urls import path

from .views import TrackViewSet, TrackCommentViewSet, TrackCommentDetailViewSet, TrackLikeViewSet, TrackLikeListViewSet, TrackMeViewSet

app_name = 'track'

urlpatterns = [
    path('', TrackViewSet.as_view({'get':'list', 'post': 'create'})),
    path('<int:track_id>/', TrackViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('<int:track>/comments/', TrackCommentViewSet.as_view({'get':'list', 'post': 'create'})),
    path('<int:track>/comments/<int:pk>/', TrackCommentDetailViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('<int:track>/like/', TrackLikeViewSet.as_view({'post':'create'})),
    path('on-stage/', TrackViewSet.as_view({'get':'on_stage'})),
    path('open-mic/', TrackViewSet.as_view({'get':'open_mic'})),
    path('likes/list/', TrackLikeListViewSet.as_view({'get':'list'})),
    path('me/', TrackMeViewSet.as_view({'get':'me'})),
    path('me/count/', TrackMeViewSet.as_view({'get':'get_count'})),
    path('me/on-stage/', TrackMeViewSet.as_view({'get':'on_stage'})),
    path('me/open-mic/', TrackMeViewSet.as_view({'get':'open_mic'})),
]