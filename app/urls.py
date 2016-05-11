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
    url(r'^delete_img/(?P<id>[0-9]+)/$', login_required(views.delete_tree_image), name='delete_img'),
    url(r'^delete_tree/(?P<id>[0-9]+)/$', login_required(views.delete_tree), name='delete_tree'),
    url(r'^logout$',
        auth_views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
]