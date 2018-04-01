from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class DogSerializer(serializers.ModelSerializer):
    """This serializes the Dog model"""

    class Meta:
        fields = (
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
            'id'
        )
        model = models.Dog


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # This initializes UserPref for the user
        models.UserPref(user=user).save()

        # This initializes UserDog objects for the user
        dog_query = models.Dog.objects.all()
        for dog in dog_query:
            models.UserDog(
                user=user,
                dog=dog,
                status='u').save()

        return user

    class Meta:
        model = get_user_model()


class UserPrefSerializer(serializers.ModelSerializer):
    """This serializes the UserPref model"""
    class Meta:
        fields = (
            'age',
            'gender',
            'size'
        )
        model = models.UserPref
