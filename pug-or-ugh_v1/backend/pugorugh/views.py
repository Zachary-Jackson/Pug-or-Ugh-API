from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
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
        """Returns the UserPref object for the logged in User"""
        return self.get_queryset().get(user=self.request.user)


class RetrieveDogView(generics.RetrieveAPIView):
    """This view returns the next dog based on the the pk and status pks"""
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        """Gets all UserDog models from the logged in User and filters the
        results based on liked, disliked, or undecided"""
        dog_status = self.kwargs.get('status_pk')
        # gets down_status down to one letter like the database
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

        # we find the current dog's index location so we can use the next
        # pk in the list
        found_index = found_pks.index(int(pk))

        try:
            dog_pk = found_pks[found_index + 1]
        except IndexError:
            return False
        else:
            return dog_query.get(pk=dog_pk)

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
        pk = self.kwargs.get('dog_pk')

        new_status = self.kwargs.get('status_pk')
        new_status = new_status[:1]

        dog = self.get_queryset().filter(pk=pk)

        # This finds the UserDog associated with the dog an User
        user_dog_query = models.UserDog.objects.filter(user=self.request.user)
        user_dog = user_dog_query.get(dog=dog)

        user_dog.status = new_status
        user_dog.save()
        return dog
