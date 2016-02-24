from django.conf.urls import include, url


urlpatterns = [
    # API
    url(r'^', include('volunteer.apps.events.api.v2.urls')),
    url(r'^', include('volunteer.apps.shifts.api.v2.urls')),
    url(r'^', include('volunteer.apps.departments.api.v2.urls')),
]
