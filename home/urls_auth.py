from django.urls import path, include
from django.conf import settings

from .views_auth import FacebookLogin, NaverLogin, KakaoLogin
from .views_auth import index, LogoutView, get_user_token, callback_comp, soundcloud_register
from accounts.views import login_cancelled

urlpatterns = [
    path('', index, name='index'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/naver/', NaverLogin.as_view(), name='nb_login'),
    path('rest-auth/kakao/', KakaoLogin.as_view(), name='ka_login'),


    path('accounts/social/login/cancelled/', login_cancelled),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-user-token/', get_user_token, name='get_user_token'),

    path('callback/', callback_comp),
    path('sc-register/<access_token>/', soundcloud_register),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
