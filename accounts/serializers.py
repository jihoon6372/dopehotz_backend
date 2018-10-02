from rest_framework import serializers
from accounts.models import Profile, User
from tracks.models import Track, TrackComment
from allauth.socialaccount.models import SocialAccount
from django.db.models import Sum

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
            'likes_greeting',
            'nickname',
            'soundcloud_id',
            'crew',
            'location'
        )

        read_only_fields = (
            'soundcloud_url',
            'profile_picture'
        )

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('provider',)


class UserSerializerBase(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    # socialaccount = SocialAccountSerializer(read_only=True)

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


class UserSerializer(UserSerializerBase):
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


class UserMeSerializer(UserSerializerBase):
    # socialaccount = SocialAccountSerializer(read_only=True)
    social_type = serializers.SerializerMethodField() 
    track_list_count = serializers.SerializerMethodField()
    user_track_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'profile',
            'social_type',
            'track_list_count',
            'user_track_info'
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

    def get_social_type(self, obj):
        return obj.socialaccount_set.first().provider.upper()


    def get_track_list_count(self, obj):
        all_count = Track.objects.filter(user=obj).count()
        on_stage_count = Track.objects.filter(user=obj, on_stage=1).count()
        open_mic_count = Track.objects.filter(user=obj, on_stage=0).count()

        result = {
            'all': all_count,
            'on_stage': on_stage_count,
            'open_mic': open_mic_count
        }
        return result

    def get_user_track_info(self, obj):
        total_play_count = Track.objects.filter(user=obj).aggregate(Sum('play_count'))
        total_like_count = Track.objects.filter(user=obj).aggregate(Sum('like_count'))
        total_comment_count = TrackComment.objects.filter(track__user=obj).count()
        
        result = {
            'play_count': 0 if None is total_play_count['play_count__sum'] else total_play_count['play_count__sum'],
            'like_count': 0 if None is total_like_count['like_count__sum'] else total_like_count['like_count__sum'],
            'comment_count': total_comment_count
        }
        return result