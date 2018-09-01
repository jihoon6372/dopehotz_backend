from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import get_next_redirect_url

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        next_url = request.session.get('next')
        from rest_auth.utils import jwt_encode
        token = jwt_encode(request.user)

        request.session['JWP_TOKEN'] = token
        
        if next_url:
            path = next_url
        else:
            path = settings.LOGIN_REDIRECT_URL
        
        return path.format(username=request.user.username)