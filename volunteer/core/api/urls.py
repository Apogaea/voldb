from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    # API
    url(r'^v2/', include('volunteer.core.api.v2.urls', namespace='v2')),
)
