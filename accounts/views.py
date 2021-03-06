from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.permissions import IsAuthenticated


from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, UserMeSerializer
from .permissions import IsOwnerOrReadOnly
# from home.permissions import IsAuthenticated


def login_cancelled(request):
    return redirect('/')



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    User = get_user_model()
    # queryset = User.objects.prefetch_related('profile').select_related('track').all()
    queryset = User.objects.prefetch_related('profile').all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    


class UserMeViewSet(viewsets.ModelViewSet):
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)

    @list_route()
    def me(self, request, *args, **kwargs):
        User = get_user_model()
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    def get_soundcloud_token(self, request, *args, **kwargs):
        try:
            return Response({'SOUNDCLOUD_OAUTH_TOKEN': request.user.soundcloudinfo.token})
        except:
            raise Http404

    

