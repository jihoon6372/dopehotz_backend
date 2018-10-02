from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Max

from .serializers import PlayListGroupSerializer, PlayListGroupDetailSerializer, PlayListUpdateSerializer
from .models import PlayListGroup, PlayList
from tracks.models import Track
from home.permissions import IsAuthenticated, BlacklistPermission
from rest_framework.exceptions import NotAuthenticated
from home.exceptions import InvalidAPIQuery


import json

class PlayListGroupViewSet(viewsets.ModelViewSet):
    serializer_class = PlayListGroupSerializer
    queryset = PlayListGroup.objects.prefetch_related('play_list__track__user__profile').all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
        )

        return Response(serializer.data)

    
    def list(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            raise NotAuthenticated()

        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PlayListGroupDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)



class PlayListViewSet(viewsets.ModelViewSet):
    serializer_class = PlayListUpdateSerializer
    permission_classes = (IsAuthenticated, BlacklistPermission, )
    queryset = PlayListGroup.objects.prefetch_related('play_list__track__user__profile').all()

    def update(self, request, pk=None):
        instance = self.get_object()
        data = request.data.get('data', None)
      
        if data is not None:
            try:
                datas = json.loads(data)

                if type(datas) is list:
                    
                    for data in datas:
                        _id = data['id']
                        order = data.get('order', False)
                        is_delete = data.get('is_delete', False)

                        try:
                            obj = PlayList.objects.get(id=_id)
                            if obj.group_id == pk:
                                if is_delete:
                                    obj.delete()
                                else:
                                    obj.order = order
                                    obj.save()

                        except PlayList.DoesNotExist:
                            return Response({"detail": "찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            except:
                raise InvalidAPIQuery('데이터가 누락 되었거나 JSON 형식이 잘못 되었습니다.')

        return Response()
    

    def create(self, request, *args, **kwargs):
        track_id = request.data.get('track', False)

        # 플레이리스트 그룹이 있는지 확인
        try:
            group = PlayListGroup.objects.get(pk=kwargs['pk'])
        
        except:
            return Response({"detail": "해당 플레이리스트 그룹을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


        # 트랙이 있는지 체크 후 있으면 플레이리스트에 삽입
        try:
            track = Track.objects.get(track_id=track_id)
            next_order_id = PlayList.objects.filter(group_id=kwargs['pk']).aggregate(Max('order'))

            if next_order_id['order__max'] is not None:
                ordering = next_order_id['order__max']+1
            else:
                ordering = 1
            
            PlayList.objects.create(group_id=kwargs['pk'], track_id=track.id, order=ordering)

            return Response({"detail": "Success"})
            

        except:
            return Response({"detail": "찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Success"})