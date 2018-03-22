from django.contrib.auth import get_user_model

from rest_framework import generics, permissions

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
        query = self.get_queryset()
        current_user = self.request.user
        filtered_queryset = query.filter(user=current_user)

        # If the current_user does not have a UserPref model
        # this will initialize it for the user
        if len(filtered_queryset) == 0:
            models.UserPref(user=current_user).save()
            query = self.get_queryset()
            filtered_queryset = query.filter(user=current_user)

        # Getting the index 0 of the queryset returns the queryset as a
        # single item for the AngularJS application
        return filtered_queryset[0]
