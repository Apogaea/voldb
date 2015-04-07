from django.conf.urls import patterns, url

from volunteer.apps.shifts.admin import views


urlpatterns = patterns(
    '',
    url(
        r'^roles/$',
        views.AdminRoleListView.as_view(),
        name='role-list',
    ),
    url(
        r'^roles/create-new/$',
        views.AdminRoleCreateView.as_view(),
        name='role-create',
    ),
    url(
        r'^roles/(?P<pk>\d+)/$',
        views.AdminRoleDetailView.as_view(),
        name='role-detail',
    ),
)
