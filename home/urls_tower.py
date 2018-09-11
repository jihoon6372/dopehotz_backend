from django.urls import path, include
from django.conf import settings

from .views_tower import *

urlpatterns = [
    path('', index, name='index'),
    path('mytracks/<list_type>/', mytracks),
    path('post/', post),
    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard),
    path('post/select/', post_select, name='post_select'),
    path('post/new/<int:track_id>/', post_new),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
