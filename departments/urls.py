from django.conf.urls import patterns, url
from departments import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
 	url(r'^(?P<department_id>\d+)/$', views.detail, name='detail'), 
)