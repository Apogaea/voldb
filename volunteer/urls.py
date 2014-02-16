from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'volunteer.views.home', name='home'),
    url(r'^$', 'volunteer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^shifts/', include('shifts.urls')),
	url(r'^departments/', include('departments.urls')),
	url(r'^accounts/', include('accounts.urls')),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
