from django.conf.urls import patterns, url
from shifts.views import GridView


urlpatterns = patterns('',  # NOQA
    url(r'^$', GridView.as_view(), name='shifts'),
#    url(r'^claim/(?P<pk>\w+)/$', ClaimView.as_view(), name='claim-shift'),
#    url(r'^release/(?P<pk>\w+)/$', ReleaseView.as_view(), name='release-shift')
)
