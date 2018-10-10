from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, permissions
from rest_framework.response import Response

from . import models
from . import serializers

# The following are age constants for dogs
BABY = list(range(0, 9))
YOUNG = list(range(9, 21))
ADULT = list(range(21, 96))
SENIOR = list(range(96, 480))


def age_range_list(ages):
    """Takes a list of desired ages and uses the age constants to return
    a list of integers"""
    age_list = []
    if 'b' in ages:
        age_list.extend(BABY)
    if 'y' in ages:
        age_list.extend(YOUNG)
    if 'a' in ages:
        age_list.extend(ADULT)
    if 's' in ages:
        age_list.extend(SENIOR)
    return age_list


def pk_intersection_finder(query_1, query_2):
    """This takes two querysets and finds the intersection between the two
    queries pks. One query needs a dog.pk attribute and the other .pk)
    Returns a list."""
    query_1_pks = set()
    for item in query_1:
        query_1_pks.add(item.dog.pk)

    query_2_pks = set()
    for item in query_2:
        query_2_pks.add(item.pk)

    return list(query_1_pks.intersection(query_2_pks))


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
        """This figures out the next dog by pk and filtered by UserPref
         or returns False"""
        pk = self.kwargs.get('dog_pk')

        user_pref = models.UserPref.objects.get(user=self.request.user)
        desired_age_range = age_range_list(user_pref.age.split(','))

        dog_query = models.Dog.objects.filter(
            age__in=desired_age_range,
            gender__in=user_pref.gender.split(','),
            size__in=user_pref.size.split(',')
            )

        # We get all the pks that match UserPref and the desired dog_status
        found_pks = pk_intersection_finder(self.get_queryset(), dog_query)

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

    def get(self, request, dog_pk, status_pk, format=None):
        """Gets the next Dog object or returns 404"""
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

        try:
            dog = self.get_queryset().get(pk=pk)
        except ObjectDoesNotExist:
            return False
        else:
            return dog

    def put(self, request, dog_pk, status_pk, format=None):
        """Tries to update the UserDog object or returns 404"""
        dog = self.get_object()
        if dog:
            new_status = self.kwargs.get('status_pk')
            new_status = new_status[:1]

            user_dog = models.UserDog.objects.get(
                user=self.request.user, dog=dog)

            user_dog.status = new_status
            user_dog.save()

            serializer = serializers.DogSerializer(dog)
            return Response(serializer.data)
        return Response(status=404)


class RetrieveUpdateUserPrefView(generics.RetrieveUpdateAPIView):
    """This view allows users to update and get user preferences"""
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        """Returns the UserPref object for the logged in User"""
        return self.get_queryset().get(user=self.request.user)
