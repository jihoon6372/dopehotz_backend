from django.urls import path

from .views import *

app_name = 'track'

urlpatterns = [
    path('', TrackViewSet.as_view({'get':'list', 'post': 'create'})),
    path('<int:track_id>/', TrackViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('<int:track>/comments/', TrackCommentViewSet.as_view({'get':'list', 'post': 'create'})),
    path('<int:track>/comments/<int:pk>/', TrackCommentDetailViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    path('<int:track>/like/', TrackCountViewSet.as_view({'post':'create'}), {'count_type': 'like'}),
    path('<int:track>/play/', TrackCountViewSet.as_view({'post':'create'}), {'count_type': 'play'}),
    path('<int:track>/view/', TrackCountViewSet.as_view({'post':'create'}), {'count_type': 'view'}),
    path('on-stage/', TrackViewSet.as_view({'get':'on_stage'})),
    path('open-mic/', TrackViewSet.as_view({'get':'open_mic'})),
    path('likes/list/', TrackLikeListViewSet.as_view({'get':'list'})),
    path('me/', TrackMeViewSet.as_view({'get':'me'})),
    path('me/count/', TrackMeViewSet.as_view({'get':'get_count'})),
    path('me/on-stage/', TrackMeViewSet.as_view({'get':'on_stage'})),
    path('me/open-mic/', TrackMeViewSet.as_view({'get':'open_mic'})),
    path('search/tag/<tag>/', TrackViewSet.as_view({'get':'tag_search'})),
    path('search/keyword/<keyword>/', TrackViewSet.as_view({'get': 'search'})),
]