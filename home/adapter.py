from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import get_next_redirect_url
from rest_auth.utils import jwt_encode
from tld import get_tld
import re

    
class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        next_url = request.session.get('next')
        del request.session['next']

        if next_url:
            localhost = re.compile('localhost')
            token = jwt_encode(request.user)

            if localhost.search(next_url):
                path = 'http://localhost:8080/#/auth/{}'.format(token)
            else:
                try:
                    detail_url = get_tld(next_url, as_object=True)
                    if detail_url.subdomain in ['tower', 'local.tower']:
                        path = '{}://{}.{}/#/auth/{}'.format(detail_url.parsed_url.scheme, detail_url.subdomain, detail_url.fld, token)
                    else:
                        path = next_url
                except:
                    path = next_url
        else:
            path = settings.LOGIN_REDIRECT_URL
        
        return path.format(username=request.user.username)