from django.conf.urls import patterns, url

from volunteer.apps.accounts.admin import views


urlpatterns = patterns('',  # NOQA
    url(r'^users/$', views.AdminUserListView.as_view(), name='user-list'),
)
