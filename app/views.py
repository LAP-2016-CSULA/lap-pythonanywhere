"""
Definition of views. 
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from datetime import datetime
from .models import Question, DailyUpdate, Tree, BirdObservation, Bird, TreeSpecies
from .serializers import *

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
# need this for getting userinfo
from oauth2_provider.oauth2_backends import get_oauthlib_core
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import os

#filter
import django_filters


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

class BirdFilter(django_filters.FilterSet):
    """A filter for the bird view"""
    type_id = django_filters.NumberFilter(name='type__id')
    type_name = django_filters.CharFilter(name='type__name', lookup_type='iexact')

    class Meta:
        model = Bird

class BirdViewSet(viewsets.ModelViewSet):
    """Viewset for the birds"""
    permission_classes = []
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    filter_class = BirdFilter

    def get_serializer_class(self):
        action_List = ['create', 'update']
        if self.action in action_List:
            return BirdSetterSerializer
        else:
            return BirdSerializer

class TreeSpeciesFilter(django_filters.FilterSet):
    """A filter for the tree species view"""
    type_id = django_filters.NumberFilter(name='typr__id')
    type_name = django_filters.CharFilter(name='type__name', lookup_type='iexact')

class TreeSpeciesViewSet(viewsets.ModelViewSet):
    """The viewset for the tree species"""
    permission_class = []
    queryset = TreeSpecies.objects.all()
    serializer_class = TreeSpeciesSerializer
    filter_class = TreeSpeciesFilter

    def get_serializer_class(self):
        action_list = ['create', 'update']
        if self.action in action_list:
            return TreeSpeciesSetterSerializer   
        else:
            return TreeSpeciesSerializer

# function based view
@api_view(['GET', 'POST'])
def userinfo(request):
    """ Check whether the user is an admin or not. """
    # from django-oauth-toolkit source code
    oauthlib_core = get_oauthlib_core()
    # oauthli_core.verify_request return valid/not valid and the processed request
    valid, r = oauthlib_core.verify_request(request, scopes=[])
    if valid:
        serializer = UserSerializer(r.user)
        return Response(serializer.data)
    return Response({})


class RegistrationView(APIView):
    permission_classes = []
    required_scopes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = User.objects.create(username=data['username'], email=data['email'])
            # Use set_password() to hash raw password
            user.set_password(data['password'])
            user.save()
            return Response({'status' : 'success'})
        return Response({'status' : 'false'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class DailyUpdateViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    queryset = DailyUpdate.objects.all()
    serializer_class = DailyUpdateSerializer

    def get_serializer_class(self):
        action_list = ['create', 'update']
        if self.action in action_list:
            return DailyUpdateSetterSerializer
        else:
            return DailyUpdateSerializer

class BirdObservationViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = BirdObservation.objects.all()
    serializer_class = BirdObservationSerializer

    def get_serializer_class(self):
        action_list = ['create', 'update']
        if self.action in action_list:
            return BirdObservationSetterSerializer
        else:
            return BirdObservationSerializer

class TreeViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer

    def get_serializer_class(self):
        action_list = ['create', 'update']
        if self.action in action_list:
            return TreeSetterSerializer
        else:
            return TreeSerializer


