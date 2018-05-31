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


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'profile'
        )