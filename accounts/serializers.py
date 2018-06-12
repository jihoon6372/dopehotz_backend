from rest_framework import serializers
from accounts.models import Profile, User
from tracks.models import Track

from home.serializers import TimeSetSerializer

class UserTrackSerializer(TimeSetSerializer):

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
            'track_score',
            'on_stage',
            'created_at'
        )

        read_only_fields = (
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
            'track_score',
            'on_stage',
            'created_at'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile

        fields = (
            'soundcloud_url',
            'profile_picture',
            'greeting',
            'clips_greeting',
            'likes_greeting'
        )

        read_only_fields = (
            'soundcloud_url',
            'profile_picture'
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    track = UserTrackSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile',
            'track'
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', False)
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if profile_data:
            profile.greeting = profile_data.get('greeting', profile.greeting)
            profile.clips_greeting = profile_data.get('clips_greeting', profile.clips_greeting)
            profile.likes_greeting = profile_data.get('likes_greeting', profile.likes_greeting)
            profile.save()

        return instance