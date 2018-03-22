from django.contrib.auth import get_user_model

from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.authtoken.models import Token

from . import models
from . import serializers


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateUserPrefView(generics.RetrieveUpdateAPIView):
    """This view allows users to update and get user prefrences"""
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        # The key argument in current_user is the token for the User test
        query = self.get_queryset()
        current_user = self.request.user
        filtered_queryset = query.filter(user=current_user)
        # getting the index 0 of the queryset returns the queryset as a
        # single item instead of a list
        return filtered_queryset[0]
