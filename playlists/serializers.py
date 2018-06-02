from home.serializers import TimeSetSerializer

from .models import PlayList, PlayListGroup


# 플레이리스트 시리얼라이저
class PlayListSerializer(TimeSetSerializer):
    class Meta:
        model = PlayList

        fields = (
            'id',
            'track',
            'order',
            'created_at'
        )

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


# 플레이리스트 그룹 디테일 시리얼라이저
class PlayListGroupDetailSerializer(PlayListGroupSerializer):
    # play_list = PlayListSerializer()

    class Meta:
        model = PlayListGroup

        fields = (
            'id',
            'user',
            'name',
            'play_list',
            'created_at'
        )