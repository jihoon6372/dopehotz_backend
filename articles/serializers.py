from home.serializers import TimeSetSerializer
from .models import Notice, Report
from accounts.serializers import UserSerializer

# 공지사항 시리얼라이저
class NoticeSerializer(TimeSetSerializer):
    
    class Meta:
        model = Notice
        fields = (
            'id',
            'user',
            'title',
            'slug',
            'content',
            'created_at'
		)


# 신고하기 시리얼라이저
class ReportSerializer(TimeSetSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'user',
            'content',
            'created_at'
        )

    
