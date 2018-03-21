from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    """This is the model for a dog"""
    name = models.CharField(max_length=100)
    image_filename = models.ImageField()
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    size = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    """This is the class that links dogs with Users"""
    user = models.OneToOneField(User)
    dog = models.ManyToManyField(Dog)
    # status is whether a User likes a dog or not. 'l' for like or 'd'
    # for disliked.
    status = models.CharField(max_length=1)

    def __str__(self):
        return self.user.username + "'s dogs"


class UserPref(models.Model):
    """This class sets a User's preference about a dog"""
    user = models.OneToOneField(User)
    age = models.CharField(max_length=7)
    gender = models.CharField(max_length=3)
    size = models.CharField(max_length=8)

    def __str__(self):
        return self.user.username + "'s dog preferences"
