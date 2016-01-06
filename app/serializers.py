"""
Model serializers for rest api.
"""

from . import models
from rest_framework import permissions, routers, serializers, viewsets


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Species


class SpeciesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpeciesType


