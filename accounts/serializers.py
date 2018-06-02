from rest_framework import serializers
from accounts.models import Profile, User

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

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile'
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