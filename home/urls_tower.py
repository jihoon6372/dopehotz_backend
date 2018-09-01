from django.urls import path, include
from django.conf import settings

from .views_tower import *

urlpatterns = [
    path('', index, name='index'),
    path('mytracks/', mytracks),
    path('post/', post),
    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard),
    path('post/select/', post_select),
    path('post/new/', post_new),
    # path('connect/', connect, name='sc_connect'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
