"""
Model serializers for rest api.
"""

from . import models
from rest_framework import permissions, routers, serializers, viewsets

from django.contrib.auth.models import User, Group

class SpeciesTypeSerializer(serializers.ModelSerializer):
    """Seralizer for the Species type"""
    class Meta:
        model = models.SpeciesType

class BirdSetterSerializer(serializers.ModelSerializer):
    """POST Serializer of Species"""
    class Meta:
        model = models.Bird

class BirdSerializer(serializers.ModelSerializer):
    """Serializer for the Bird module"""
    type = SpeciesTypeSerializer(read_only=True)

    class Meta:
        model = models.Bird

class TreeSpeciesSetterSerializer(serializers.ModelSerializer):
    """POST Serializer for Tree Species"""
    class Meta:
        model = models.TreeSpecies

class TreeSpeciesSerializer(serializers.ModelSerializer):
    """Serializer for the Tree Species module"""
    type = SpeciesTypeSerializer(read_only=True)

    class Meta:
        model = models.TreeSpecies

class TreeSerializer(serializers.ModelSerializer):
    """ Serializer of Tree. """
    species = TreeSpeciesSerializer(read_only=True)
    changed_by = serializers.StringRelatedField()

    class Meta:
        model = models.Tree

class TreeSetterSerializer(serializers.ModelSerializer):
    """ POST Serializer of Tree. """
    class Meta:
        model = models.Tree
        exclude = ('image', 'changed_by',)

class ChoiceSerializer(serializers.ModelSerializer):
    """ Get Serializer of choice. """
    question = serializers.StringRelatedField()
    class Meta:
        model = models.Choice


class ChoiceSetterSerializer(serializers.ModelSerializer):
    """ Question choice update serializer """
    class Meta:
        model = models.Choice



# django-oauth-toolkkit tutorial
class UserSerializer(serializers.ModelSerializer):
    """ Serializer of User. It excludes id and password. """
    class Meta:
        model = User
        exclude = ('id', 'password')


class GroupSerializer(serializers.ModelSerializer):
    """ ??? """
    class Meta:
        model = Group


class RegistrationSerializer(serializers.ModelSerializer):
    """ Serializer of Registering User. It should only contains some information. """
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


# http://stackoverflow.com/questions/14978464/django-rest-nested-object-add-on-create-post-not-just-update-put
class DailyUpdateSerializer(serializers.ModelSerializer):
    """ Serializer of Daily Update. """
    choices = ChoiceSerializer(many=True)
    birds = BirdSerializer(many=True)
    changed_by = serializers.StringRelatedField()

    class Meta:
        model = models.DailyUpdate


class DailyUpdateSetterSerializer(serializers.ModelSerializer):
    """ Serializer of daily update. This one is used in post. """
    class Meta:
        model = models.DailyUpdate
        exclude = ('changed_by',)


class QuestionSerializer(serializers.ModelSerializer):
    """ Serializer of Question. """
    choices = ChoiceSerializer(source='choice_set', many=True, read_only=True)
    class Meta:
        model = models.Question


class CheckDBChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DBLastChangeTime
        exclude = ('id',)

class CheckDBChangeSetterSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField()
    class Meta:
        model = models.DBLastChangeTime
        exclude = ('type', 'id',)

class CheckDBSerializer(serializers.Serializer):
    db_was_changed = serializers.BooleanField()
    list = serializers.ReturnList


class DateTimeSerializer(serializers.Serializer):
    time = serializers.DateTimeField()


class DeleteTreeSerializer(serializers.ModelSerializer):
    """ Deleted Tree serializer """
    class Meta:
        model = models.DeletedTree
        exclude = ('id',)