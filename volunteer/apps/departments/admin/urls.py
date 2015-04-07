from django.conf.urls import patterns, url

from volunteer.apps.departments.admin import views


urlpatterns = patterns(
    '',
    url(
        r'^departments/$', views.AdminDepartmentListView.as_view(),
        name='department-list',
    ),
    url(
        r'^departments/create-new/$',
        views.AdminDepartmentCreateView.as_view(), name='department-create',
    ),
    url(
        r'^departments/(?P<pk>\d+)/$',
        views.AdminDepartmentDetailView.as_view(), name='department-detail',
    ),
    url(
        r'^departments/(?P<department_pk>\d+)/roles/create-new/$',
        views.AdminRoleCreateView.as_view(),
        name='role-create',
    ),
    url(
        r'^departments/(?P<department_pk>\d+)/roles/(?P<pk>\d+)/$',
        views.AdminRoleDetailView.as_view(),
        name='role-detail',
    ),
)
