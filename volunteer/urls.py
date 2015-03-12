from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',  # NOQA
    url(
        '^robots.txt$', TemplateView.as_view(
            content_type='text/plain', template_name='robots.txt',
        ),
    ),
    # Examples:
    url(r'^$', 'volunteer.core.views.home', name='home'),

    # Views
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shifts/', include('volunteer.apps.shifts.urls')),
    url(r'^departments/', include('volunteer.apps.departments.urls')),
    url(r'^accounts/', include('volunteer.apps.accounts.urls')),

    # API
    url(r'^api/', include('volunteer.core.api.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
