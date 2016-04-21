from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from app.forms import BootstrapAuthenticationForm
from datetime import datetime

# This file contains the urls for website
# namespace for app
app_name = 'web'

urlpatterns = [
    url(r'^$', login_required(views.UserIndexView.as_view()), name='index'),
    url(r'^(?P<username>\w{0,50})/$', login_required(views.UserDetailView.as_view()), name='detail'),
]