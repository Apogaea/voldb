from django.conf.urls import patterns, url
from accounts.views import (
    RegisterView, RegisterSuccessView, RegisterConfirmView, ProfileView,
)


urlpatterns = patterns('',  # NOQA
    url(r'^/$', ProfileView.as_view(), name='profile'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(
        r'^register/success/$', RegisterSuccessView.as_view(),
        name='register_success',
    ),
    url(
        r'^register/(?P<token>[-a-zA-Z0-9_:]+)/$',
        RegisterConfirmView.as_view(),
        name='register_confirm',
    ),
)
urlpatterns += patterns(
    'authtools.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(r'^password-reset/$', 'password_reset', name='password_reset'),
    url(
        r'^password-reset-done/$', 'password_reset_done',
        name='password_reset_done',
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm_and_login',
        name='password_reset_confirm',
    ),
    url(
        r'^password-reset-complete/$', 'password_reset_complete',
        name='password_reset_complete',
    ),
)
