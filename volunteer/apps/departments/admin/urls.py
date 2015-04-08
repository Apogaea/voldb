from django.conf.urls import patterns, url, include

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
        r'^departments/(?P<pk>\d+)/merge-with-other-department/$',
        views.AdminDepartmentMergeView.as_view(), name='department-merge',
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
    url(
        r'^departments/(?P<department_pk>\d+)/roles/(?P<pk>\d+)/merge-with-other-role/$',
        views.AdminRoleMergeView.as_view(),
        name='role-merge',
    ),
    # Shifts admin
    url(
        r'^departments/(?P<department_pk>\d+)/roles/(?P<role_pk>\d+)/',
        include('volunteer.apps.shifts.admin.urls'),
    ),
)
