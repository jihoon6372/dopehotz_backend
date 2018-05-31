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


from accounts.models import User
from post.models import Post
def get_user(request):
    user_list = Post.objects.select_related('user__profile').all()

    return render(request, 'test.html', {'user_list':user_list})