"""
Model serializers for rest api.
"""

from . import models
from rest_framework import permissions, routers, serializers, viewsets

from django.contrib.auth.models import User, Group


class SpeciesTypeSerializer(serializers.ModelSerializer):
    """ Serializer of Species Type. """
    class Meta:
        model = models.SpeciesType


class SpeciesSerializer(serializers.ModelSerializer):
    """ Serializer of Spcies. """
    #type = serializers.SlugRelatedField(slug_field='name', queryset=models.SpeciesType.objects.all())
    type = SpeciesTypeSerializer(read_only=True)
    class Meta:
        model = models.Species
        # depth = 1


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


class DailyUpdateSerializer(serializers.ModelSerializer):
    """ Serializer of Daily Update. """
    class Meta:
        model = models.DailyUpdate


class QuestionSerializer(serializers.ModelSerializer):
    """ Serializer of Question. """
    class Meta:
        model = models.Question


class TreeSerializer(serializers.ModelSerializer):
    """ Serializer of Tree. """
    class Meta:
        model = models.Tree