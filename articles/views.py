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
        # 타입 입력 체크
        if 'report_type' not in request.data:
            return Response({'report_type' : ['이 필드는 필수 항목입니다.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            report_type = int(request.data.get('report_type'))
        except:
            return Response({'report_type' : ['지원되지 않는 타입입니다.']}, status=status.HTTP_400_BAD_REQUEST)

        # 저장
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            report_type_id=report_type
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)