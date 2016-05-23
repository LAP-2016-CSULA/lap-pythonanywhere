"""
Definition of views. 
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from datetime import datetime
from .models import Question, DailyUpdate, Tree, Bird, TreeSpecies, SpeciesType
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
from django.utils.dateparse import parse_datetime
from django.views import generic
from django.http import HttpResponseRedirect

def index(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app/index.html')

def treemap(request):
    "Render the page with a google map"
    #tree = TreeSpecies.objects.order_by('name')
    assert isinstance(request, HttpRequest)
    return render(request, 'app/map.html')

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
    type_name = django_filters.CharFilter(name='type__name')

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


class TreeSpeciesViewSet(viewsets.ModelViewSet):
    """The viewset for the tree species"""
    permission_classes = []
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = TreeSpecies.objects.all()
    serializer_class = TreeSpeciesSerializer

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
    """ Registration view """
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
    """ Checking what were changed in the DB """
    permission_classes = []
    required_scopes = []

    def get(self, request):
        """ Get the list of latest change timestamps of all models """
        queryset = models.DBLastChangeTime.objects.all()
        if queryset:
            serializer = CheckDBChangeSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({})

    def post(self, request):
        """ Get the list of latest change models after a specified timestamps """
        serializer = CheckDBChangeSetterSerializer(data=request.data)
        if serializer.is_valid():
            time = serializer.validated_data.get('time', None)
            if not time:
                return Response({})
            queryset = models.DBLastChangeTime.objects.filter(time__gt=time)
            if queryset:
                serializer = CheckDBChangeSerializer(queryset, many=True)
                return Response(serializer.data)
        return Response({})


class UserViewSet(viewsets.ModelViewSet):
    """ Gonna be removed later??? """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """ ??? """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """ Question Viewset. Returns json """
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class DailyUpdateFilter(django_filters.FilterSet):
    """ A filter for the dailyupdate viewset. """
    changed_by = django_filters.CharFilter(name='changed_by__username', lookup_type='iexact')
    time = django_filters.DateTimeFilter(name='date_of_observation', lookup_type='gt')

    class Meta:
        model = DailyUpdate


class DailyUpdateViewSet(viewsets.ModelViewSet):
    """ DailyUpdate viewset. Returns json """
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    queryset = DailyUpdate.objects.all()
    serializer_class = DailyUpdateSerializer
    filter_class = DailyUpdateFilter

    def get_serializer_class(self):
        action_list = ['create', 'update']
        if self.action in action_list:
            return DailyUpdateSetterSerializer
        else:
            return DailyUpdateSerializer

    def perform_create(self, serializer):
        auto_user(self, serializer)

    def perform_update(self, serializer):
        auto_user(self, serializer)


class TreeFilter(django_filters.FilterSet):
    """ A filter for the tree viewset. """
    changed_by = django_filters.CharFilter(name='changed_by__username', lookup_type='iexact')
    time = django_filters.DateTimeFilter(name='date_modified', lookup_type='gt')

    class Meta:
        model = Tree


class TreeViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    filter_class = TreeFilter

    def get_serializer_class(self):
        action_list = ['create', 'update']
        if self.action in action_list:
            return TreeSetterSerializer
        else:
            return TreeSerializer

    def perform_create(self, serializer):
        auto_user(self, serializer)

    def perform_update(self, serializer):
        auto_user(self, serializer)


def auto_user(obj, serializer):
    """
    This method adds the user (whether authenticated user or guest) to serializer and save it.
    The models must contain a django.contrib.auth.models.User field named 'changed_by'.
    It should be called in ViewSet's perform_create and perform_update.
    It is best to exclude User from the serializer (request's data) when using this method
    """
    if obj.request.user.is_authenticated():
        serializer.save(changed_by=self.request.user)
    else:
        user = get_or_create_guest_user()
        serializer.save(changed_by=user)

def get_or_create_guest_user():
    """
    Try to get the 'guest' user. If 'guest' is not found in the database, create new one
    and return it.
    """
    try:
        guest = User.objects.get(username='guest')
    except User.DoesNotExist:
        guest = User.objects.create(username='guest', email='this_is_guest_email@calstatela.edu')
        # Use set_password() to hash raw password
        guest.set_password('guest_password')
        guest.save()
    return guest


class DeletedTreeFilter(django_filters.FilterSet):
    """ Filter for deleted trees. mostly by time """
    time = django_filters.DateTimeFilter(name='time', lookup_type='gt')

    class Meta:
        model = models.DeletedTree


class DeletedTreeView(APIView):
    """ Deleted trees viewset """
    permission_classes = []
    serializer_class = DeleteTreeSerializer
    #queryset = models.DeletedTree.objects.all()
    filter_class = DeletedTreeFilter
    
    def get(self, request):
        """ Get the list of deleted trees """
        time = self.request.query_params.get('time', None)
        if time:
            #time = parse_datetime(param)
            queryset = models.DeletedTree.objects.filter(time__gt=time)
        else:
            queryset = models.DeletedTree.objects.all()
        if queryset:
            serializer = DeleteTreeSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({})


class UserIndexView(generic.ListView):
    """ List of classes/groups """
    template_name = 'app/user_index.html'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Group.objects.all()
        else:
            return self.request.user.groups.all()


class UserDetailView(generic.ListView):
    """ List of user's tree """
    template_name = 'app/user_detail.html'

    def get_queryset(self):
        if 'username' in self.kwargs:
            if not self.request.user.is_staff:
                return HttpResponseRedirect(reverse('web:detail') + '/' + self.request.user.username)
            name = self.kwargs['username']
            try:
                u = User.objects.get(username=name)
                du_list = models.DailyUpdate.objects.filter(changed_by=u).prefetch_related('tree')
                tree_set = {du.tree for du in du_list}
                return tree_set
            except ObjectDoesNotExist:
                return None
        else:
            return None


def delete_tree_image(request, id):
    """ Delete a tree's image"""
    if request.user.is_staff:
        t = get_object_or_404(Tree, pk=id)
        if t.image and os.path.isfile(t.image.path):
            os.remove(t.image.path)
        t.image = None
        t.save()
    return redirect(request.META.get('HTTP_REFERER'))


def delete_tree(request, id):
    """ Delete a tree from database """
    if request.user.is_staff:
        t = get_object_or_404(Tree, pk=id).delete()
    return redirect(request.META.get('HTTP_REFERER'))