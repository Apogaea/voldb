from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from authtools.views import PasswordChangeView

from volunteer.apps.accounts import views


urlpatterns = patterns(
    '',
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^edit/$', views.ProfileUpdateView.as_view(), name='profile-edit'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(
        r'^register/success/$', views.RegisterSuccessView.as_view(),
        name='register-success',
    ),
    url(
        r'^register/(?P<token>[-a-zA-Z0-9_:]+)/$',
        views.RegisterConfirmView.as_view(),
        name='register-confirm',
    ),
)
urlpatterns += patterns(
    'authtools.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(
        r'^change-password/$', PasswordChangeView.as_view(
            template_name='accounts/change_password.html',
            success_url=reverse_lazy('dashboard'),
        ), name='password-change',
    ),
    url(r'^password-reset/$', 'password_reset', name='password-reset'),
    url(
        r'^password-reset-done/$', 'password_reset_done',
        name='password-reset-done',
    ),
    url(
        r'^password-reset-done/$', 'password_reset_done',
        name='password_reset_done',  # authtools uses underscore view names.
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm_and_login',
        name='password-reset-confirm-and-login',
    ),
    url(
        r'^password-reset-complete/$', 'password_reset_complete',
        name='password-reset-complete',
    ),
    url(
        r'^password-reset-complete/$', 'password_reset_complete',
        name='password_reset_complete',  # authtools uses underscore view names.
    ),
)
