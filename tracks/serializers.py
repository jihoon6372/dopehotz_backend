from rest_framework import serializers
from .models import Track, TrackComment

from accounts.serializers import UserSerializer 


class CommentChildSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = TrackComment
		fields =(
			'id',
			'user',
			'content',
			'created_at'
		)

class CommentSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)	
	children = CommentChildSerializer(read_only=True, many=True)
	created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

	class Meta:
		model = TrackComment
		fields = (
			'id',
			'user',
			'children',
			'content',
			'created_at'
		)

		read_only_fields = (
			'user',
			'created_at'
		)





class TrackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)


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

