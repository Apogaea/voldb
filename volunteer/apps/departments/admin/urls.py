from django.conf.urls import patterns, url

from volunteer.apps.departments.admin import views


urlpatterns = patterns(
    '',  # NOQA
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
)
