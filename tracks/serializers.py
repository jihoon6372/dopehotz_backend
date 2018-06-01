from .models import Track, TrackComment
from home.serializers import TimeSetSerializer
from accounts.serializers import UserSerializer 


# 대댓글 시리얼라이저 (replies)
class CommentChildSerializer(TimeSetSerializer):
	user = UserSerializer(read_only=True)

	class Meta:
		model = TrackComment
		fields =(
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
            'parent',
			'content',
			'created_at'
		)


# 트랙 시리얼라이저
class TrackSerializer(TimeSetSerializer):
    user = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True, many=True)

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
			'likes',
			'track_score',
			'on_stage',
			'comment',
            'created_at'
        )

        read_only_fields = (
			'slug',
			'view_count',
			'likes',
			'track_score',
			'on_stage',
			'genre',
			'image_url',
			'download_url',
			'waveform_url'
        )

