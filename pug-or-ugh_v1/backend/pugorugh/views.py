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


class RetrieveUndecidedDogView(generics.RetrieveAPIView):
    """This view returns an dog that the user is undecided on"""
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        pk = self.kwargs.get('dog_pk')
        # This if statement temporarly negates the -1 React is giving in the
        # url http://localhost:8000/api/dog/-1/undecided/next/
        # and just defaults to a pk of 1 for now.
        # Will get an index error if no dogs in database
        if pk == '1':
            return self.queryset.filter(id=1)[0]
        return self.queryset.filter(id=self.kwargs.get('dog_pk'))[0]
        # return self.queryset.filter(id=1)[0]
