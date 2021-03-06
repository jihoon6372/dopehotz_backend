from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from django.db.models import Prefetch, Q

from .serializers import TrackSerializer, CommentSerializer, CommentCreateSerializer, CommentSerializer_v2, TrackLikeSerializer, TrackLikeListSerializer, TrackPlaySerializer, TrackViewSerializer
from .models import Track, TrackComment, TrackLikeLog, TrackViewLog, TrackPlayLog
from home.permissions import IsOwnerOrReadOnly
from home.exceptions import InvalidAPIQuery

import requests

def soundcloud_track_data(track_id):
    return requests.get('http://api.soundcloud.com/tracks/'+str(track_id)+'?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY).json()


# 트랙 뷰셋
class TrackViewSet(viewsets.ModelViewSet):
    lookup_field = 'track_id'
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Track.objects.prefetch_related(Prefetch('comment', queryset=TrackComment.objects.filter(parent=None)), 'comment__user__profile', 'comment__children__user__profile', 'tracks_tracklikelog_track').select_related('user__profile').filter(is_deleted=False)

    def create(self, request, *args, **kwargs):        
        track_type = request.data.get('track_type', '')
        
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

        return data
        

    def update(self, request, *args, **kwargs):
        if 'track_id' in request.data:
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

    
    def list(self, request, *args, **kwargs):
        queryset = self.set_queryset_order_by(self.filter_queryset(self.get_queryset()))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

    @list_route()
    def on_stage(self, request, *args, **kwargs):      
        queryset = self.get_queryset().filter(on_stage=1)
        queryset = self.set_queryset_order_by(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @list_route()
    def open_mic(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(on_stage=0)
        queryset = self.set_queryset_order_by(queryset)
        
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

        # 상업적 공개여부 체크
        if 'distribute' not in request.data:
            return Response({'distribute' : ['이 필드는 필수 항목입니다.']}, status=status.HTTP_400_BAD_REQUEST)   

        # 수정 및 배포여부 체크
        if 'public' not in request.data:
            return Response({'public' : ['이 필드는 필수 항목입니다.']}, status=status.HTTP_400_BAD_REQUEST)   
        
        # 사운드클라우드 트랙 데이터 가져오기
        sc_data = soundcloud_track_data(request.data['track_id'])

        # 사운드클라우드의 게시물이 존재하는지 체크
        if 'errors' in sc_data:
            return Response({'message' : '사운드클라우드의 게시물을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 사운드클라우드의 트랙이 게시자의 트랙게시물인지 체크
        if sc_data['user']['id'] != request.user.profile.soundcloud_id:
            return Response({'message' : '사운드클라우드의 본인 트랙 게시물만 등록 가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 기타 저장용 데이터 가져오기
        genre = sc_data.get('genre', '')
        download_url = sc_data.get('download_url', '')
        waveform_url = sc_data.get('waveform_url', '')
        duration = sc_data.get('duration', '')
        is_distribute = request.data.get('distribute')
        is_public = request.data.get('public')

        if None is sc_data['artwork_url']:
            image_url = sc_data['user']['avatar_url']
        else:
            image_url = sc_data['artwork_url']


        # 저장
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            genre=genre,
            image_url=image_url,
            download_url = download_url,
            waveform_url = waveform_url,
            duration = duration,
            api_id = 1,
            is_public = is_public,
            is_distribute = is_distribute
        )

        return Response(serializer.data)
        # return serializer.data

    @list_route()
    def me(self, request, *args, **kwargs):
        print(request.user)
        return Response({'a':'aa'})

    
    def set_queryset_order_by(self, queryset):
        order = self.request.GET.get('order', None)
        order_type = self.request.GET.get('order_type', None)

        if order_type is not None:
            asc_or_desc = ''

            if 'desc' in order:
                asc_or_desc = '-'

            if 'play' in order_type:
                order_by = '{}play_count'.format(asc_or_desc)

            if 'like' in order_type:
                order_by = '{}like_count'.format(asc_or_desc)

            queryset = queryset.order_by(order_by)
        
        return queryset

    
    @list_route()
    def tag_search(self, request, *args, **kwargs):
        tag = kwargs['tag'].replace(' ', '')

        if 0 is len(tag):
            raise InvalidAPIQuery('검색어를 올바르게 입력하세요.')
        
        queryset = self.get_queryset().filter(tag__contains=tag)
        queryset = self.set_queryset_order_by(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def search(self, request, *args, **kwargs):
        keyword = kwargs['keyword'].replace(' ', '')

        if 0 is len(keyword):
            raise InvalidAPIQuery('검색어를 올바르게 입력하세요.')

        queryset = self.get_queryset().filter(Q(tag__contains=keyword) | Q(title__contains=keyword))
        queryset = self.set_queryset_order_by(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





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



# 트랙 좋아요, 조회, 플레이 뷰셋
class TrackCountViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if 'like' is kwargs['count_type']:
            set_serializer = eval('TrackLikeSerializer')

        elif 'play' is kwargs['count_type']:
            set_serializer = eval('TrackPlaySerializer')

        elif 'view' is kwargs['count_type']:
            set_serializer = eval('TrackViewSerializer')

        serializer = set_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'count': self.count}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        track = get_object_or_404(Track, track_id=self.kwargs['track'])

        q = {}
        if 'like' is self.kwargs['count_type']:
            queryset = TrackLikeLog.objects
            count_column_name = 'like_count'

        elif 'play' is self.kwargs['count_type']:
            queryset = TrackPlayLog.objects
            count_column_name = 'play_count'

        elif 'view' is self.kwargs['count_type']:
            queryset = TrackViewLog.objects
            count_column_name = 'view_count'

        log, is_create = queryset.get_or_create(user=self.request.user, track=track)

        if is_create == False and 'like' is self.kwargs['count_type']:
            log.delete()

        self.count = queryset.filter(track=track).count()
        q[count_column_name] = self.count
        
        Track.objects.filter(track_id=self.kwargs['track']).update(**q)


# 트랙 좋아요 한 리스트 가져오기
class TrackLikeListViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TrackLikeListSerializer
    queryset = TrackLikeLog.objects.select_related('track').all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 트랙 ME
class TrackMeViewSet(viewsets.ModelViewSet):
    serializer_class = TrackSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Track.objects.prefetch_related(Prefetch('comment', queryset=TrackComment.objects.filter(parent=None)), 'comment__user__profile', 'comment__children__user__profile', 'tracks_tracklikelog_track').select_related('user__profile').filter(is_deleted=False)
    
    def me(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        queryset = self.set_queryset_order_by(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def on_stage(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user, on_stage=1)
        queryset = self.set_queryset_order_by(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def open_mic(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user, on_stage=0)
        queryset = self.set_queryset_order_by(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def set_queryset_order_by(self, queryset):
        order = self.request.GET.get('order', None)
        order_type = self.request.GET.get('order_type', None)

        if order_type is not None:
            asc_or_desc = ''

            if 'desc' in order:
                asc_or_desc = '-'

            if 'play' in order_type:
                order_by = '{}play_count'.format(asc_or_desc)

            if 'like' in order_type:
                order_by = '{}like_count'.format(asc_or_desc)

            queryset = queryset.order_by(order_by)
        
        return queryset