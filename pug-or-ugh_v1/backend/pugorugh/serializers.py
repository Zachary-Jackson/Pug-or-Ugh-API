from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class DogSerializer(serializers.ModelSerializer):
    """This serializes the Dog model"""
    # For id see get_id
    id = serializers.SerializerMethodField()
    
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

    # This get_id is a test to see how the React program operates. Will
    # delete later on. If I set this to return 2 the React program goes to
    # pk of 2 (after viewing the first pk) and PUTs to pk of 2 on the
    # RetrieveUndecidedDogView even if I am actually viewing the first pk.
    def get_id(self, obj):
        return '2'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
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
