from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.contrib.auth import get_user_model

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from home.permissions import IsOwnerOrReadOnly

def login_cancelled(request):
    return redirect('/')



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    queryset = get_user_model().objects.prefetch_related('profile').all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @list_route()
    def me(self, request, *args, **kwargs):
        User = get_user_model()
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    

