from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from django.dispatch import receiver

def api_view(request):
    return HttpResponse('Api Server OK')


def auth_view(request):
    return HttpResponse('Auth Server OK')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer




from tracks.models import TrackComment, Track
from django.db.models import Prefetch, Q
def get_user(request):
    # tracks = Track.objects.prefetch_related(Prefetch('comment__children', queryset=TrackComment.objects.filter(parent=None))).get(pk=14)
    # tracks = Track.objects.prefetch_related('comment__children', Prefetch('comment', to_attr='comment')).get(pk=14)
    tracks = Track.objects.prefetch_related('comment__children', Prefetch('children', queryset=TrackComment.objects.filter(parent=None) )).get(pk=14)
    # tracks

    # user_list = Post.objects.select_related('user__profile').all()

    return render(request, 'test.html', {'tracks':tracks})

def get_user2(request):
    comments = TrackComment.objects.prefetch_related('children').filter(parent=None)
    # user_list = Post.objects.select_related('user__profile').all()

    return render(request, 'test.html', {'comments':comments})