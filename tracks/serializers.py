from .models import Track, TrackComment
from home.serializers import TimeSetSerializer
from accounts.serializers import UserSerializer 


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

		read_only_fields = (
			'user',
			'children',
			'created_at'
		)


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

		read_only_fields = (
			'user',
			'created_at'
		)


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
            'user',
			'slug',
			'view_count',
			'likes',
			'track_score',
			'on_stage',
			'genre',
			'image_url',
			'download_url',
			'waveform_url',
            'created_at'
        )

