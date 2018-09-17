"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from rest_framework_jwt.views import refresh_jwt_token

from .views import UserViewSet, get_user

urlpatterns = [
    path('token/refresh/', refresh_jwt_token),
    path('v1/tracks/', include('tracks.urls', namespace='v1:track')),
    path('v1/accounts/', include('accounts.urls', namespace='v1:accounts')),
    path('v1/playlist/', include('playlists.urls', namespace='v1:playlist')),
    path('v2/tracks/', include('tracks.urls', namespace='v2:track')),
    path('discord/', include('discord_bot.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
