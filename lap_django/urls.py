"""
Definition of urls for lap_django. 
"""

from datetime import datetime
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from app.forms import BootstrapAuthenticationForm
from django.contrib import admin
from django.contrib.auth import views
from app.views import *
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from django.conf.urls import include

# Routers
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'dailyupdates', DailyUpdateViewSet)
router.register(r'trees', TreeViewSet)
router.register(r'birds', BirdViewSet)
router.register(r'treespecies', TreeSpeciesViewSet)

urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),
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

    #Site urls
    url(r'^trees', include('app.urls')),

    # django-oauth-toolkit
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include(router.urls)),
    # custom API
<<<<<<< HEAD
    url(r'^api/userinfo', userinfo, name='userinfo'),
    url(r'^api/register', RegistrationView.as_view(), name='register'),
    url(r'^api/checkdb', CheckDBChangeView.as_view(), name='checkdb'),
    url(r'^api/deletedtrees', DeletedTreeView.as_view(), name='deletedtrees'),
    url(r'^web/', include('app.urls')),
=======
    url(r'^userinfo', userinfo, name='userinfo'),
    url(r'^register', RegistrationView.as_view(), name='register'),
    url(r'^checkdb', CheckDBChangeView.as_view(), name='checkdb'),
    url(r'deletedtrees', DeletedTreeView.as_view(), name='deletedtrees'),
    url(r'/', include('app.urls')),
>>>>>>> a47289a6b97ab4ae81c29870817026e63d464427
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


