"""
Definition of urls for lap_django.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm
from django.contrib import admin
from django.contrib.auth import views
from app.views import *
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()


# Routers
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'species', SpeciesViewSet)
# router.register(r'userinfo', userinfo)


urlpatterns = [
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', contact, name='contact'),
    url(r'^about', about, name='about'),
    url(r'^login/$',
        views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # django-oauth-toolkit
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^', include(router.urls)),
    url(r'userinfo', userinfo, name='userinfo'),
]


