from django.contrib.auth import get_user_model

from rest_framework import generics, status, permissions
from rest_framework.response import Response

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


class RetrieveDogView(generics.RetrieveAPIView):
    """This view returns the next dog based on the the pk and status pks"""
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        pk = self.kwargs.get('dog_pk')

        dog_status = self.kwargs.get('status_pk')
        dog_status = dog_status[:1]

        query = self.get_queryset().filter(user=self.request.user)
        dog_query = models.Dog.objects.all()

        # This initializes a UserDog for each dog for the User
        # if this has not been completed already
        if len(query) == 0:
            for dog in dog_query:
                models.UserDog(
                    user=self.request.user,
                    dog=dog,
                    status='u').save()
            query = self.get_queryset().filter(user=self.request.user)

        # This gets a list of pks for dogs matching the status_pk
        found_pks = []
        for item in query:
            if item.status == dog_status:
                found_pks.append(item.dog.pk)

        if pk == '-1':
            return dog_query.get(pk=found_pks[0])

        pk = int(pk)
        found_index = found_pks.index(pk)

        # Currently causes an IndexError and makes the React app work
        # properly. Could find better solution.
        dog_pk = found_pks[found_index + 1]
        return dog_query.get(pk=dog_pk)
