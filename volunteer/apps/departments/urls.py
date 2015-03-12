from django.conf.urls import patterns, url
from departments import views


urlpatterns = patterns('',  # NOQA
    url(r'^$', views.DepartmentListView.as_view(), name='department_list'),
    url(
        r'^(?P<pk>\d+)/$', views.DepartmentDetailView.as_view(),
        name='department_detail',
    ),
)
