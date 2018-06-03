from home.serializers import TimeSetSerializer

from .models import PlayList, PlayListGroup
from tracks.models import Track
from tracks.serializers import TrackSerializerBySimple


# 플레이리스트 그룹 시리얼라이저
class PlayListGroupSerializer(TimeSetSerializer):
    class Meta:
        model = PlayListGroup

        fields = (
            'id',
            'name',
            'created_at'
        )

# 플레이리스트 시리얼라이저
class PlayListSerializer(TimeSetSerializer):
    track = TrackSerializerBySimple()
    class Meta:
        model = PlayList

        fields = (
            'id',
            'track',
            'order',
            'created_at'
        )

# 플레이리스트 그룹 디테일 시리얼라이저
class PlayListGroupDetailSerializer(PlayListGroupSerializer):
    play_list = PlayListSerializer(many=True)

    class Meta:
        model = PlayListGroup

        fields = (
            'id',
            'user',
            'name',
            'play_list',
            'created_at'
        )