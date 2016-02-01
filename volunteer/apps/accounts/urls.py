from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from authtools.views import (
    PasswordChangeView,
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmAndLoginView,
    PasswordResetCompleteView,
)

from volunteer.apps.accounts import views


urlpatterns = patterns(
    '',
    url(r'^$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^(?P<pk>\d+)/$', views.PublicProfileView.as_view(), name='public-profile'),
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
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(
        r'^change-password/$', PasswordChangeView.as_view(
            template_name='accounts/change_password.html',
            success_url=reverse_lazy('dashboard'),
        ), name='password-change',
    ),
    url(r'^password-reset/$', PasswordResetView.as_view(), name='password-reset'),
    url(
        r'^password-reset-done/$', PasswordResetDoneView.as_view(),
        name='password-reset-done',
    ),
    url(
        r'^password-reset-done/$', PasswordResetDoneView.as_view(),
        name='password_reset_done',  # authtools uses underscore view names.
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmAndLoginView.as_view(),
        name='password-reset-confirm-and-login',
    ),
    url(
        r'^password-reset-complete/$', PasswordResetCompleteView.as_view(),
        name='password-reset-complete',
    ),
    url(
        r'^password-reset-complete/$', PasswordResetCompleteView.as_view(),
        name='password_reset_complete',  # authtools uses underscore view names.
    ),
)
