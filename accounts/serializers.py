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
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile'
        )