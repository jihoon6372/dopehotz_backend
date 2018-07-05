from django.urls import path, include
from django.conf import settings

from .views_tower import index

urlpatterns = [
    path('', index, name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
