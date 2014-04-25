from django.conf.urls import patterns, url
from organizations import views


urlpatterns = patterns('',  # NOQA
    url(r'^$', views.OrganizationListView.as_view(), name='organization_list'),
    url(r'^create/$', views.OrganizationCreateView.as_view(), name='organization_create'),
    url(
        r'^(?P<pk>\d+)/$', views.OrganizationDetailView.as_view(),
        name='organization_detail',
    ),
    url(
        r'^(?P<pk>\d+)/edit/$', views.OrganizationUpdateView.as_view(),
        name='organization_update',
    ),
    url(
        r'^(?P<pk>\d+)/manage-members/$', views.OrganizationManageMembersView.as_view(),
        name='organization_manage_members',
    ),
    url(
        r'^(?P<pk>\d+)/manage-requests/$', views.OrganizationManageRequestsView.as_view(),
        name='organization_manage_requests',
    ),
    # Joining
    url(
        r'^(?P<pk>\d+)/join/$', views.OrganizationJoinView.as_view(),
        name='organization_join',
    ),
    url(
        r'^(?P<pk>\d+)/join/success/$', views.OrganizationJoinSuccessView.as_view(),
        name='organization_join_success',
    ),
)
