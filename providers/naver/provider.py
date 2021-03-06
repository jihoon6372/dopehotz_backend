from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class NaverAccount(ProviderAccount):

    def get_avatar_url(self):
        return self.account.extra_data.get('profile_image')

    def to_str(self):
        return self.account.extra_data.get('nickname', self.account.uid)


class NaverProvider(OAuth2Provider):
    id = 'naver'
    name = 'Naver'
    account_class = NaverAccount

    def sociallogin_from_response(self, request, response):
        sociallogin = super(NaverProvider, self).sociallogin_from_response(request, response)
        if not sociallogin.user.username:
            sociallogin.user.username = 'naver_%s' % sociallogin.account.extra_data['id']
        return sociallogin

    def extract_uid(self, data):
        return str(data['id'])


provider_classes = [NaverProvider]
