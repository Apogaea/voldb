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
    url(r'^$', 'volunteer.views.home', name='home'),

    # Views
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shifts/', include('shifts.urls')),
    url(r'^departments/', include('departments.urls')),
    url(r'^accounts/', include('accounts.urls')),

    # API
    url(r'^api/v2/', include('shifts.api.v2.urls')),
    url(r'^api/', include('shifts.api.urls')),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
