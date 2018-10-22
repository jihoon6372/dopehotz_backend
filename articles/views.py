from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers import NoticeSerializer, ReportSerializer
from .models import Notice, Report
from home.permissions import IsOwnerOrReadOnly

class NoticeViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = NoticeSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Notice.objects.filter(is_delete=False)


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Report.objects

    def create(self, request, *args, **kwargs):

        # 저장
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)