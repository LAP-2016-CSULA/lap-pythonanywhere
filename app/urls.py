from django.conf.urls import url

from . import views

app_name = 'web'
urlpatterns = [
    url(r'^$', views.UserIndexView.as_view(), name='index'),
    url(r'^(?P<username>\w{0,50})/$', views.UserDetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]