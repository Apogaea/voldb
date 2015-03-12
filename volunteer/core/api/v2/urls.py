from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    # API
    url(r'^', include('volunteer.apps.shifts.api.v2.urls')),
    url(r'^', include('volunteer.apps.departments.api.v2.urls')),
)
