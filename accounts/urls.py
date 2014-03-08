from django.conf.urls import patterns, url
from departments import views
from authtools.views import LoginView, LogoutView
from accounts.views import RegisterView


urlpatterns = patterns('',  # NOQA
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
)
