from home.serializers import TimeSetSerializer

from .models import PlayList, PlayListGroup

# 플레이리스트 그룹 시리얼라이저
class PlayListGroupSerializer(TimeSetSerializer):
    class Meta:
        model = PlayListGroup

        fields = (
            'id',
            'user',
            'name',
            'created_at'
        )

        read_only_fields = (
            'user',
        )
