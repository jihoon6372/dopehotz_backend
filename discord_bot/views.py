from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils import timezone

from .models import *
from .serializers import DiscordLogSerializer
from home.permissions import IsAllAuthenticated

class DiscordLogView(viewsets.ModelViewSet):
    serializer_class = DiscordLogSerializer
    permission_classes = (IsAllAuthenticated,)
    queryset = DiscordLog.objects.all()

    def list(self, request, *args, **kwargs):
        range_hour = int(request.GET.get('hour', 1))
        now_filter = timezone.now() - timezone.timedelta(hours=range_hour)
        queryset = self.get_queryset().filter(created_at__gt=now_filter)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)