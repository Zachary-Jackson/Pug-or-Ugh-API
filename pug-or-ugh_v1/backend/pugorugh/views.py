from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, permissions
from rest_framework.response import Response

from . import models
from . import serializers


class UserRegisterView(generics.CreateAPIView):
    """This view creates a user"""
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class RetrieveDogView(generics.RetrieveAPIView):
    """This view returns the next dog based on the the pk and status pks"""
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        """Gets all UserDog models from the logged in User and filters the
        results based on liked, disliked, or undecided"""
        dog_status = self.kwargs.get('status_pk')
        # gets dog_status down to one letter like the database
        dog_status = dog_status[:1]

        return self.queryset.filter(user=self.request.user, status=dog_status)

    def get_object(self):
        """This figures out the next dog by pk or returns False"""
        pk = self.kwargs.get('dog_pk')

        found_pks = []
        for userdog in self.get_queryset():
            found_pks.append(userdog.dog.pk)

        dog_query = models.Dog.objects.all()

        # The react app starts finding dogs with a -1 pk
        if pk == '-1':
            try:
                return dog_query.get(pk=found_pks[0])
            except IndexError:
                return False

        # figures out the next dog by pk
        next_pk = False
        for number in found_pks:
            if number > int(pk):
                next_pk = number
                break

        if next_pk:
            return dog_query.get(pk=next_pk)
        return False

    def get(self, reqest, dog_pk, status_pk, format=None):
        dog = self.get_object()
        if dog:
            serializer = serializers.DogSerializer(dog)
            return Response(serializer.data)
        return Response(status=404)


class UpdateUserDogView(generics.UpdateAPIView):
    """This view allows for UserDog to be updated"""
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        """Gets the Dog object from the database or returns False"""
        pk = self.kwargs.get('dog_pk')

        new_status = self.kwargs.get('status_pk')
        new_status = new_status[:1]

        try:
            dog = self.get_queryset().get(pk=pk)
        except ObjectDoesNotExist:
            return False
        else:
            return dog

    def put(self, request, dog_pk, status_pk, format=None):
        dog = self.get_object()
        if dog:
            new_status = self.kwargs.get('status_pk')
            new_status = new_status[:1]

            user_dog = models.UserDog.objects.get(user=self.request.user, dog=dog)

            user_dog.status = new_status
            user_dog.save()

            serializer = serializers.DogSerializer(dog)
            return Response(serializer.data)
        return Response(status=404)


class RetrieveUpdateUserPrefView(generics.RetrieveUpdateAPIView):
    """This view allows users to update and get user prefrences"""
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        """Returns the UserPref object for the logged in User"""
        return self.get_queryset().get(user=self.request.user)
