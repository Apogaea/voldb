from django.conf.urls import patterns, url
from shifts.views import GridView

urlpatterns = patterns('',
    url(r'^$', GridView.as_view(), name='grid')
)