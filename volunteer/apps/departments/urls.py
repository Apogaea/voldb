from django.conf.urls import patterns, url

from volunteer.apps.departments import views


urlpatterns = patterns(
    '',
    url(r'^$', views.DepartmentListView.as_view(), name='department-list'),
    url(
        r'^(?P<pk>\d+)/$', views.DepartmentDetailView.as_view(),
        name='department-detail',
    ),
)
