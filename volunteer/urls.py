from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',  # NOQA
    # Examples:
    url(r'^$', 'volunteer.views.home', name='home'),

    # Views
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shifts/', include('shifts.urls')),
    url(r'^departments/', include('departments.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^profiles/', include('profiles.urls')),

    # API
    url(r'^api/', include('shifts.api.urls')),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
