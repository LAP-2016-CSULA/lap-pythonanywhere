"""
Model serializers for rest api.
"""

from . import models
from rest_framework import permissions, routers, serializers, viewsets

from django.contrib.auth.models import User, Group

class SpeciesSerializer(serializers.ModelSerializer):
    """ Serializer of Spcies. """
    class Meta:
        model = models.Species


class SpeciesTypeSerializer(serializers.ModelSerializer):
    """ Serializer of Species Type. """
    class Meta:
        model = models.SpeciesType


# django-oauth-toolkkit tutorial
class UserSerializer(serializers.ModelSerializer):
    """ Serializer of User. It excludes id and password. """
    class Meta:
        model = User
        exclude = ('id', 'password')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class RegistrationSerializer(serializers.ModelSerializer):
    """ Serializer of Registering User. It should only contains some information. """
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

