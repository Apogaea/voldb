from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    # API
    url(r'^', include('shifts.api.v2.urls')),
    url(r'^', include('departments.api.v2.urls')),
)
