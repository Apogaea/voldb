from django.conf.urls import patterns, url
from shifts import views


urlpatterns = patterns('',  # NOQA
    url(r'^$', views.ShiftAppView.as_view(), name='shifts'),
    url(r'^leaderboard/$', views.LeaderBoardView.as_view(), name='leaderboard'),
)
