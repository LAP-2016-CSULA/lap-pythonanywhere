"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import Species
from .serializers import SpeciesSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

# need this for getting userinfo
from oauth2_provider.oauth2_backends import get_oauthlib_core

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
    # permission_classes = [permissions.IsAuthenticated]
    # required_scopes = []
    # from django-oauth-toolkit source code
    oauthlib_core = get_oauthlib_core()
    # oauthli_core.verify_request return valid/not valid and the processed request
    valid, r = oauthlib_core.verify_request(request, scopes=[])
    if valid:
        # return whether the user is a superuser
        return Response({'is_admin' : str(r.user.is_superuser)})
    return Response({})
