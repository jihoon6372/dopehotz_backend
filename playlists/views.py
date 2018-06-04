from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import PlayListGroupSerializer, PlayListGroupDetailSerializer, PlayListUpdateSerializer
from .models import PlayListGroup, PlayList
from home.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from home.exceptions import InvalidAPIQuery

import json

# from rest_framework import permissions
class PlayListGroupViewSet(viewsets.ModelViewSet):
    serializer_class = PlayListGroupSerializer
    queryset = PlayListGroup.objects.prefetch_related('play_list__track__user__profile').all()
    permission_classes = (IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)

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
        serializer = PlayListGroupDetailSerializer(instance)
        return Response(serializer.data)

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PlayListUpdateSerializer(instance)

        data = request.data.get('list', None)
        if data is not None:
            try:
                data = json.loads(data)
                if type(data) is list:
                    print('list형')
            except:
                raise InvalidAPIQuery('JSON 형식이 잘못 되었습니다.')

        return Response({'data':'dd'})


# import json
class PlayListUpdateViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def update(self, request, pk=None):
        data = request.data.get('list', None)
        
        data = json.loads(data)
        print(data)
        if data is not None:
            data = json.loads(data)
            if type(data) is list:
                print('list형')
                

        return Response({'test':'a'})


from django.http import HttpResponse

def test(requets):
    data = [
        {
            'track' : '100001',
            'order' : 1
        },
        {
            'track' : '100002',
            'order' : 2
        },
        {
            'track' : '100003',
            'is_delete' : True
        }
    ]

    data = json.dumps(data)
    return HttpResponse(data)