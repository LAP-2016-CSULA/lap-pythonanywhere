"""
Model serializers for rest api.
"""

from . import models
from rest_framework import permissions, routers, serializers, viewsets

from django.contrib.auth.models import User, Group

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Species


class SpeciesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpeciesType


# django-oauth-toolkkit tutorial
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group

