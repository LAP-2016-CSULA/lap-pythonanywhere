"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from datetime import datetime
from .models import Species, Question, DailyUpdate, Tree
from .models import get_db_last_change_time
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


class SpeciesFilter(django_filters.FilterSet):
    """ Special filter for species view. """
    type_id = django_filters.NumberFilter(name='type__id')
    type_name = django_filters.CharFilter(name='type__name', lookup_type='iexact')

    class Meta:
        model = Species
        

class SpeciesViewSet(viewsets.ModelViewSet):
    permission_classes = []
    required_scopes = []
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filter_class = SpeciesFilter

    def get_serializer_class(self):
        action_list = ['create', 'update']
        if self.action in action_list:
            return SpeciesSetterSerializer
        else:
            return SpeciesSerializer

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


class CheckDBChangeView(APIView):
    permission_classes = []
    required_scopes = []

    def get(self, request):
        #serializer = CheckDBChangeSerializer()
        queryset = models.DBLastChangeTime.objects.all()
        if queryset:
            serializer = CheckDBChangeSerializer(queryset, many=True)
        #if last_change_time_object:
        #    serializer = CheckDBChangeSerializer(last_change_time_object)
            return Response(serializer.data)
        else:
            return Response({})

    def post(self, request):
        serializer = CheckDBChangeSerializer(data=request.data)
        if serializer.is_valid():
            last_change_time_object = get_db_last_change_time()
            time = serializer.validated_data.get('time', None)
            if time < last_change_time_object.time:
               return Response({'db_was_changed' : 'true'})
        return Response({'db_was_change' : 'false'})

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


