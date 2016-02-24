from django.conf.urls import url

from volunteer.apps.departments import views


urlpatterns = [
    url(r'^$', views.DepartmentListView.as_view(), name='department-list'),
    url(
        r'^(?P<pk>\d+)/$', views.DepartmentDetailView.as_view(),
        name='department-detail',
    ),
    url(
        r'^(?P<pk>\d+)/report/$', views.DepartmentShiftSlotReportView.as_view(),
        name='department-shift-report',
    ),
]
