from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.adapter import DefaultAccountAdapter

"""
Disable registration/signup
"""
class MyAccountAdapter(DefaultAccountAdapter):    
    def is_open_for_signup(self, request):
        return False


class User(get_user_model()):
    User = get_user_model()
    objects = User.objects.prefetch_related('profile', 'soundcloudinfo')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField('닉네임', max_length=20, blank=True)
    soundcloud_url = models.CharField('사운드클라우드 URL', max_length=255, blank=True)
    profile_picture = models.CharField('프로필 이미지 URL', max_length=255, blank=True)
    greeting = models.TextField('인사말', blank=True)
    likes_greeting = models.TextField('좋아요 인사말', blank=True)
    clips_greeting = models.TextField('구독 인사말', blank=True)
    soundcloud_id = models.BigIntegerField(default=False, blank=True, verbose_name='사운드클라우드 아이디', db_index=True)
    mailing_agree = models.BooleanField('메일 수신여부', default=False, help_text='광고성 메일 수신 동의 여부')
    crew = models.CharField('소속', max_length=100, blank=True)
    location = models.CharField('활동지역', max_length=100, blank=True)


    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = '프로필'

    def __str__(self):
        return str(self.user)


class SoundcloudInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='soundcloudinfo')
    token = models.CharField('사운드클라우드 토큰', max_length=40, blank=True)

    class Meta:
        verbose_name_plural = '사운드클라우드 계정 정보'


from allauth.account.signals import user_signed_up
@receiver(user_signed_up)
def user_signed_up_populate_user(sender, request, sociallogin, **kwargs):
    account = sociallogin.account
    data = account.extra_data
    user = account.user

    profile_image = ''

    if 'naver' in account.provider:
        user.email = data.get('email', '')
        user.first_name = data.get('nickname', '')
        profile_image = data.get('profile_image', '')

    if 'kakao' in account.provider:
        user.email = data.get('kaccount_email', '')
        user.first_name = data['properties'].get('nickname', '')
        profile_image = data['properties'].get('profile_image', '')

    user.save()

    # 프로파일 정보 추가
    Profile.objects.create(
        user=user,
        profile_picture = profile_image
    )
