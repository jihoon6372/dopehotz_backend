from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from django.db.models import Prefetch

from .serializers import TrackSerializer, CommentSerializer, CommentCreateSerializer, CommentSerializer_v2, TrackLikeSerializer
from .models import Track, TrackComment, TrackLikeLog
from home.permissions import IsOwnerOrReadOnly
from home.exceptions import InvalidAPIQuery

import requests

def soundcloud_track_data(track_id):
    return requests.get('http://api.soundcloud.com/tracks/'+track_id+'?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY).json()


# 트랙 뷰셋
class TrackViewSet(viewsets.ModelViewSet):
    lookup_field = 'track_id'
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Track.objects.prefetch_related(Prefetch('comment', queryset=TrackComment.objects.filter(parent=None)), 'comment__user__profile', 'comment__children__user__profile', 'like').select_related('user__profile').filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
        track_type = request.data.get('type', '')
        
        if not track_type:
            return Response({'track_type' : ['이 필드는 필수 항목입니다.']}, status=status.HTTP_400_BAD_REQUEST)        
            
        # 트랙 타입이 사우드클라우드일 경우 처리
        elif track_type == 'soundcloud':
            data = self.soundcloud(request, args, kwargs)
            
        # 트랙 타입이 유튜브일 경우 처리()
        elif track_type == 'youtube':
            raise InvalidAPIQuery('지원하지 않는 타입입니다.')
            
        else:
            raise InvalidAPIQuery('지원하지 않는 타입입니다.')

        
        return Response(data)
        

    def update(self, request, *args, **kwargs):
        post_id = request.data.get('track_id', '')
        if post_id and kwargs['track_id'] != post_id:
            raise InvalidAPIQuery('Track ID는 변경할 수 없습니다.')

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

    @list_route()
    def on_stage(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(on_stage=1)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        # 버전 관리
        # if self.request.version == 'v2':
        #     return TrackSerializer_v2

        return self.serializer_class

    def soundcloud(self, request, *args, **kwargs):
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
        # if sc_data['user']['id'] != request.user.profile.soundcloud_id:
        #     return Response({'message' : '사운드클라우드의 본인 트랙 게시물만 등록 가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)

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
            duration = duration,
            api = 1
        )

        # return Response(serializer.data)
        return serializer.data


# 트랙 댓글 버전관리 상속용 뷰셋
class TrackCommentVersioningViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        # 버전 관리
        if self.request.version == 'v2':
            return CommentSerializer_v2

        return self.serializer_class


# 트랙 댓글 뷰셋
class TrackCommentViewSet(TrackCommentVersioningViewSet):

    def get_queryset(self, **kwargs):
        return TrackComment.objects.prefetch_related('children__user__profile').select_related('track', 'user__profile').filter(track__track_id=self.kwargs['track'], parent=None)

    def create(self, request, *args, **kwargs):
        track = Track.objects.filter(track_id=self.kwargs['track']).first()

        if track is None:
            raise InvalidAPIQuery('트랙을 찾을 수 없습니다.')

        # 저장
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            track_id=track.id
        )

        serializer = self.list(request, order_by='desc')	# 댓글 등록시 해당 트랙의 댓글리스트 불러오는 list (요청사항인데 별로 좋지 않은방법같아 돌아갈 수 있음)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 트랙 댓글 디테일 뷰셋
class TrackCommentDetailViewSet(TrackCommentVersioningViewSet):
    queryset = TrackComment.objects.prefetch_related('children__user__profile').select_related('track', 'user__profile')

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()



# 트랙 좋아요 뷰셋
class TrackLikeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = TrackLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'count': self.like_count}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        track = get_object_or_404(Track, track_id=self.kwargs['track'])
        like_log, is_create = TrackLikeLog.objects.get_or_create(user=self.request.user, track=track)

        if is_create == False:
            like_log.delete()

        self.like_count = TrackLikeLog.objects.filter(track=track).count()