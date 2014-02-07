from django.conf.urls import patterns, url
from shifts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index') 
)