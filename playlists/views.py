from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import PlayListGroupSerializer
from .models import PlayListGroup, PlayList

class PlayListGroupViewSet(viewsets.ModelViewSet):
    serializer_class = PlayListGroupSerializer
    queryset = PlayListGroup.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
        )

        return Response(serializer.data)

    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)