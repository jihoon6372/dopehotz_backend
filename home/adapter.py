from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import get_next_redirect_url

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        next_url = request.session.get('next')
        del request.session['next']
                
        if next_url:
            path = next_url
        else:
            path = settings.LOGIN_REDIRECT_URL
        
        return path.format(username=request.user.username)