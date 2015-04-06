from django.conf.urls import patterns, url

from volunteer.apps.events.admin import views


urlpatterns = patterns('',  # NOQA
    url(r'^events/$', views.AdminEventListView.as_view(), name='event-list'),
    url(r'^events/create-new/$', views.AdminEventCreateView.as_view(), name='event-create'),
    url(r'^events/(?P<pk>\d+)/$', views.AdminEventDetailView.as_view(), name='event-detail'),
)
