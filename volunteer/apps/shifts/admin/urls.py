from django.conf.urls import patterns, url

from volunteer.apps.shifts.admin import views


urlpatterns = patterns(
    '',
    url(
        r'^shifts/create-new/$', views.AdminShiftCreateView.as_view(),
        name='shift-create',
    ),
    url(
        r'^shifts/(?P<pk>\d+)/$', views.AdminShiftDetailView.as_view(),
        name='shift-detail',
    ),
)
