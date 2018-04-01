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
        return self.get_queryset().get(user=self.request.user)


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
