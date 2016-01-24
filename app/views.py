"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from datetime import datetime
from .models import Species, Question, DailyUpdate, Tree
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


class SpeciesViewSet(viewsets.ModelViewSet):
    permission_classes = []
    required_scopes = []
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

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
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
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


# http://stackoverflow.com/questions/20473572/django-rest-framework-file-upload
class FileUploadView(APIView):
    """ Uploading picture/file. """
    parser_classes = (MultiPartParser, FormParser,)
    # TESTING: do not require authorization. will apply it later
    permission_classes = []
    required_scopes = []

    def post(self, request, format='jpg'):
        """ Get file from POST request. """
        up_file = request.FILES['file']
        with open('images/' + up_file.name, 'wb+') as destination:
            for chunk in up_file.chunks():
                destination.write(chunk)
                # destination.close()

        return Response(status=201)


class DailyImageUploadView(APIView):
    """ Image upload for daily update v2. This require daily update id. """
    parser_classes = (MultiPartParser, FormParser,)
    # permisstion_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = []
    def post(self, request, format='jpg'):
        """ Get image form POST request. """
        # Check if there is a daily update info
        try:
            id = request.data['dailyupdate_id']
            du = DailyUpdate.objects.get(pk=int(request.POST['dailyupdate_id']))
        except ObjectDoesNotExist:
            return Response({'detail' : 'provided dailyupdate_id does not exist'}, status=400)
        except MultipleObjectsReturned:
            return ResourceWarning({'detail': 'provided dailyupdate_id results in multiple objects'}, status=400)
        except Exception as err:
            return Response({'detail': 'bad dailyupdate_id; error type: ' + str(type(err))}, status=404)
        image = request.FILES['file']
        # Assume all image will be in jpg format
        check_or_create_folder('images')
        path = 'images/daily'
        if check_or_create_folder(path):
            filename = path + '/' + str(du.id) + '.jpg'
            if os.path.exists(filename):
                return Response({'detail': 'file already exists for the provided dailyupdate_id'}, status=404)
            else:
                with open(filename, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                        # destination.close()

        return Response({'detail' : 'image uploaded successfully'}, status=201)

def check_or_create_folder(path):
    """ Check if folder exists or not. Create new folder if it does not. 
        Arg:
        path (str) -- filepath to check on. """
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    if not os.path.isdir(path):
        return True
    return False
