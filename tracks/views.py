from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .serializers import TrackSerializer
from .models import Track
from home.permissions import IsOwnerOrReadOnly

import requests

def soundcloud_track_data(track_id):
    return requests.get('http://api.soundcloud.com/tracks/'+track_id+'?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY).json()

class TrackViewSet(viewsets.ModelViewSet):
    lookup_field = 'track_id'
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Track.objects.select_related('user__profile').filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
        # 사우드클라우드 계정인지 확인
        if not request.user.profile.soundcloud_id:
            return Response({'message' : '사운드클라우드 계정으로 로그인 후 이용해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 트랙 입력 체크
        if 'track_id' not in request.data:
            return Response({'track_id' : ['이 필드는 필수 항목입니다.']}, status=status.HTTP_400_BAD_REQUEST)        

        # 사운드클라우드 트랙 데이터 가져오기
        # sc_data = requests.get('http://api.soundcloud.com/tracks/'+request.data['track_id']+'?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY).json()
        sc_data = soundcloud_track_data(request.data['track_id'])

        # 사운드클라우드의 게시물이 존재하는지 체크
        if 'errors' in sc_data:
            return Response({'message' : '사운드클라우드의 게시물을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 사운드클라우드의 트랙이 게시자의 트랙게시물인지 체크
        if sc_data['user']['id'] != request.user.profile.soundcloud_id:
            return Response({'message' : '사운드클라우드의 본인 트랙 게시물만 등록 가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 기타 저장용 데이터 가져오기
        genre = sc_data.get('genre', '')
        image_url = sc_data.get('artwork_url', '')
        download_url = sc_data.get('download_url', '')
        waveform_url = sc_data.get('waveform_url', '')
        duration = sc_data.get('duration', '')


        # 저장
        serializer = TrackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            genre=genre,
            image_url=image_url,
            download_url = download_url,
            waveform_url = waveform_url,
            duration = duration
        )

        return Response(serializer.data)

    
    def update(self, request, *args, **kwargs):
        post_id = request.data.get('track_id', '')
        if post_id and kwargs['track_id'] != post_id:
            return Response({'message' : 'Track ID는 변경할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST) 

        sc_data = soundcloud_track_data(str(kwargs['track_id']))
        
        instance = self.get_object()
        instance.duration = sc_data.get('duration', 0)
        instance.save()
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.track_id = None
        instance.save()