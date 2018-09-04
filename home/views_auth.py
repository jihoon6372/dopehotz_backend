from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout as auth_logout
from django.views.generic import RedirectView
from rest_auth.registration.views import SocialLoginView
from providers.facebook.views import FacebookOAuth2Adapter
from providers.naver.views import NaverOAuth2Adapter
from providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.conf import settings
from accounts.models import SoundcloudInfo

import requests
import json


def index(request):
    request.session['next'] = request.GET.get('next', None)
    
    return render(request, 'home.html', {'HOME_URL': settings.HOME_URL})


class LogoutView(RedirectView):
	url = '//auth.dopehotz.com'

	def get(self, request, *args, **kwargs):
		auth_logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter


def get_user_token(request):
    from rest_auth.utils import jwt_encode
    
    token = jwt_encode(request.user)
    return redirect(settings.HOME_URL+'/#token='+token)

def callback_comp(request):
    return render(request, 'callback_comp.html')


def soundcloud_register(request, access_token):
    url = 'https://api.soundcloud.com/me?oauth_token='+access_token
    sc_data = requests.get(url)
    user_data = json.loads(sc_data.content)

    try:
        soundcloud_info = request.user.soundcloudinfo
    except:
        soundcloud_info = SoundcloudInfo()
        soundcloud_info.user = request.user

    soundcloud_info.token = access_token
    soundcloud_info.save()

    profile = request.user.profile
    profile.soundcloud_id = user_data['id']
    profile.soundcloud_url = user_data['permalink_url']
    profile.profile_picture = user_data['avatar_url']
    profile.save()

    return render(request, 'soundcloud_register.html')