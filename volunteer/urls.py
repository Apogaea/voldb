from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from django.conf import settings

from volunteer.core import views


urlpatterns = patterns(
    '',
    url(
        '^robots.txt$', TemplateView.as_view(
            content_type='text/plain', template_name='robots.txt',
        ),
    ),
    # Examples:
    url(r'^$', views.SiteIndexView.as_view(), name='site-index'),

    # Views
    # url(r'^admin/', include('volunteer.core.admin.urls', namespace='admin')),
    url(r'^departments/', include('volunteer.apps.departments.urls')),
    url(r'^accounts/', include('volunteer.apps.accounts.urls')),

    # API
    url(r'^api/', include('volunteer.core.api.urls')),

)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
