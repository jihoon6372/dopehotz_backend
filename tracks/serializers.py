from rest_framework import serializers

from .models import Track, TrackComment, TrackLikeLog, TrackViewLog, TrackPlayLog
from home.serializers import TimeSetSerializer
from accounts.serializers import UserSerializer


# 대댓글 시리얼라이저 (replies)
class CommentChildSerializer(TimeSetSerializer):
	user = UserSerializer(read_only=True)

	class Meta:
		model = TrackComment
		fields = (
            'id',
            'user',
            'content',
            'created_at'
		)

	def to_representation(self, instance):
		representation = super(CommentChildSerializer, self).to_representation(instance)
		if instance.is_deleted:
			representation['content'] = '삭제된 덧글 입니다.'

		return representation


# 댓글 시리얼라이저
class CommentSerializer(CommentChildSerializer):
	children = CommentChildSerializer(read_only=True, many=True)

	class Meta:
		model = TrackComment
		fields = (
            'id',
            'user',
            'content',
            'children',
            'created_at'
		)


# 댓글 버전2 (댓글 시리얼라이저 상속 후 필드만 제거)
class CommentSerializer_v2(CommentSerializer):

	class Meta:
		model = TrackComment
		fields = (
            'user',
            'content',
            'created_at'
		)


# 댓글 생성 시리얼라이저
class CommentCreateSerializer(TimeSetSerializer):
	user = UserSerializer(read_only=True)	

	class Meta:
		model = TrackComment
		fields = (
            'id',
            'user',
            'parent',
            'content',
            'created_at'
		)


class TrackSerializerBySimple(TimeSetSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Track
        fields = (
            'track_id',
            'user',
            'title',
            'tag',
            'genre',
            'duration',
            'image_url',
            'download_url',
            'waveform_url',
            'view_count',
            'track_score',
            'created_at'
        )



# 트랙 시리얼라이저
class TrackSerializer(TrackSerializerBySimple):
    comment = CommentSerializer(read_only=True, many=True)
    is_like = serializers.SerializerMethodField() 

    class Meta:
        model = Track
        fields = (
            'track_id',
            'user',
            'title',
            'slug',
            'tape_info',
            'duration',
            'lyrics',
            'tag',
            'genre',
            'image_url',
            'download_url',
            'waveform_url',
            'view_count',
            'like_count',
            'play_count',
            'track_score',
            'on_stage',
            'comment',
            'created_at',
            'is_public',
            'is_distribute',
            'is_like'
        )

        read_only_fields = (
            'slug',
            'view_count',
            'track_score',
            'on_stage',
            'genre',
            'image_url',
            'download_url',
            'waveform_url'
        )

    def get_like_count(self, obj):
        return obj.tracks_tracklikelog_track.count()

    def get_is_like(self, obj):
        return TrackLikeLog.objects.filter(track=obj, user=self.context['request'].user).exists()

        

class TrackLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackLikeLog
        fields = ('user',)
        read_only_fields = ('user',)


class TrackViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackViewLog
        fields = ('user',)
        read_only_fields = ('user',)


class TrackPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPlayLog
        fields = ('user',)
        read_only_fields = ('user',)


class OnlyTrackSerializer(TimeSetSerializer):
    class Meta:
        model = Track
        fields = (
            'track_id',
            'title',
            'tag',
            'genre',
            'image_url',
            'download_url',
            'waveform_url',
            'view_count',
            'track_score',
            'created_at'
        )

class TrackLikeListSerializer(serializers.ModelSerializer):
    track = OnlyTrackSerializer(read_only=True)

    class Meta:
        model = TrackLikeLog
        fields = ('track',)
        read_only_fields = ('track',)