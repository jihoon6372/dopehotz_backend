from rest_framework import serializers
from .models import Track

# from accounts.models import Profile, User
from accounts.serializers import UserSerializer 

class TrackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
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