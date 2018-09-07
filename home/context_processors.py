from django.conf import settings
from rest_auth.utils import jwt_encode
from tracks.models import Track

def settings_data(request):
    result_data = ''

    if request.host.urlconf == 'home.urls_tower':
        all_count = Track.objects.filter(user=request.user).count()
        on_stage_count = Track.objects.filter(user=request.user, on_stage=1).count()
        open_mic_count = Track.objects.filter(user=request.user, on_stage=0).count()

        result_data = {
            'API_URL': settings.API_URL,
            'JWT_TOKEN': jwt_encode(request.user),
            'TRACK_COUNT': {
                'all': all_count,
                'on_stage': on_stage_count,
                'open_mic': open_mic_count
            }
        }

    return result_data