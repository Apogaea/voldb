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
    url(
        r'^shifts/(?P<pk>\d+)/delete/$', views.AdminShiftDeleteView.as_view(),
        name='shift-delete',
    ),
    url(
        r'^shifts/(?P<pk>\d+)/assign-volunteer/$', views.AdminShiftSlotCreateView.as_view(),
        name='shift-slot-create',
    ),
    url(
        r'^shifts/(?P<shift_pk>\d+)/slots/(?P<pk>\d+)/$',
        views.AdminShiftSlotCancelView.as_view(),
        name='shift-slot-cancel',
    ),
)
