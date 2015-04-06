from django.conf.urls import patterns, url, include

from volunteer.core.admin import views

urlpatterns = patterns(
    '',
    # Main Admin Urls
    url(r'^$', views.AdminIndexView.as_view(), name='index'),
    # url(r'^guide/$', views.AdminGuideView.as_view(), name='guide'),
    url(r'^login/$', views.AdminLoginView.as_view(), name='login'),

    # App Admin Urls
    url(r'^', include('volunteer.apps.accounts.admin.urls')),
    url(r'^', include('volunteer.apps.events.admin.urls')),
    url(r'^', include('volunteer.apps.departments.admin.urls')),
    # url(r'^', include('volunteer.apps.shifts.admin.urls')),
)
