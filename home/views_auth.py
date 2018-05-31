from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout as auth_logout
from django.views.generic import RedirectView
from rest_auth.registration.views import SocialLoginView
from providers.facebook.views import FacebookOAuth2Adapter
from providers.naver.views import NaverOAuth2Adapter
from providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.models import SocialAccount, SocialToken

import requests
import json


def index(request):
    return render(request, 'home.html', {})


class LogoutView(RedirectView):
	url = '//auth.dopehotz.com:8000'

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
    social_account = SocialAccount.objects.get(user=request.user)
    social_token = SocialToken.objects.get(account__user=request.user, account__provider=social_account.provider)

    url = 'http://auth.dopehotz.com:8000/rest-auth/'+social_account.provider+'/'
    headers = {'content-type': 'application/json'}
    data = {'access_token': social_token.token}

    token = requests.post(url=url, data=json.dumps(data), headers=headers)
    
    if(token.status_code == 500):
        return redirect(reverse('logout'))

    token = json.loads(token.content)

    return redirect('/#token='+token['token'])