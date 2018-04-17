from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    """This is the model for a dog"""
    name = models.CharField(max_length=100)
    image_filename = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, default='unknown')

    age = models.IntegerField(
        help_text='Please enter an integer as months lived.')

    gender = models.CharField(
        max_length=1,
        help_text="Enter 'm' for male, 'f' for female")

    size = models.CharField(
        max_length=2,
        help_text=("All size options are 's,m,l,xl'" +
                   " for small, medium, large or extra large"),
        )

    def __str__(self):
        return self.name


class UserDog(models.Model):
    """This is the class that links dogs with Users"""
    user = models.ForeignKey(User)
    dog = models.ForeignKey(Dog)

    status = models.CharField(
        max_length=1,
        help_text="All status options are 'l,d,u'" +
                  " for liked, disliked, and undecided.",
        default='u')

    def __str__(self):
        return (
            'Dog: ' + self.dog.name.title() + ', User: '
            + self.user.username.title()
            )


class UserPref(models.Model):
    """This class sets a User's preference about a dog"""
    user = models.OneToOneField(User)

    age = models.CharField(
        max_length=7,
        help_text=("All age options are 'b,y,a,s'" +
                   " for baby, young, adult and senior"),
        default='b,y,a,s')

    gender = models.CharField(
        max_length=3,
        help_text=("All gender options are 'm,f' for male and female"),
        default='m,f')

    size = models.CharField(
        max_length=8,
        help_text=("All size options are 's,m,l,xl'" +
                   " for small, medium, large, and extra large"),
        default='s,m,l,xl')

    def __str__(self):
        return self.user.username.title() + "'s dog preferences"
