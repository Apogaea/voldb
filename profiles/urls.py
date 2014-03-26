from django.conf.urls import patterns, url
from profiles.views import ProfileView, ProfilesView

urlpatterns = patterns('',  # NOQA
    url(r'^$', ProfilesView.as_view(), name='profiles'),
    url(r'^(?P<pk>\w+)/$', ProfileView.as_view(), name='profile'),
)
