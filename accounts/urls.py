from django.conf.urls import patterns, url
from accounts.views import (
    RegisterView, RegisterSuccessView, RegisterConfirmView,
)


urlpatterns = patterns('',  # NOQA
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(
        r'^register/success/$', RegisterSuccessView.as_view(),
        name='register-success',
    ),
    url(
        r'^register/(?P<token>[-a-zA-Z0-9_:]+)/$',
        RegisterConfirmView.as_view(),
        name='register-confirm',
    ),
)
urlpatterns += patterns(
    'authtools.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(r'^password-reset/$', 'password_reset', name='password-reset'),
    url(
        r'^password-reset-done/$', 'password_reset_done',
        name='password-reset-done',
    ),
    url(
        r'^password-reset-confirm/(?P<uidb36>\w+)/(?P<token>[-a-zA-Z0-9]+)/$',
        'password_reset_confirm_and_login', name='password-reset-confirm',
    ),
    url(
        r'^password-reset-complete/$', 'password_reset_complete',
        name='password-reset-complete',
    ),
)
