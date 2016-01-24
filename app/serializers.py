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

class SpeciesSetterSerializer(serializers.ModelSerializer):
    """ POST Serializer of Species. """
    class Meta:
        model = models.Species

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


class ChoiceSerializer(serializers.ModelSerializer):
    """ Serializer of choice. """
    question = serializers.StringRelatedField()
    class Meta:
        model = models.Choice


class ChoiceSetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Choice


# http://stackoverflow.com/questions/14978464/django-rest-nested-object-add-on-create-post-not-just-update-put
class DailyUpdateSerializer(serializers.ModelSerializer):
    """ Serializer of Daily Update. """
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = models.DailyUpdate


class DailyUpdateSetterSerializer(serializers.ModelSerializer):
    """ Serializer of daily update. This one is used in post. """
    class Meta:
        model = models.DailyUpdate


class QuestionSerializer(serializers.ModelSerializer):
    """ Serializer of Question. """
    class Meta:
        model = models.Question


class TreeSerializer(serializers.ModelSerializer):
    """ Serializer of Tree. """
    species = SpeciesSerializer()
    class Meta:
        model = models.Tree

class TreeSetterSerializer(serializers.ModelSerializer):
    """ POST Serializer of Tree. """
    class Meta:
        model = models.Tree