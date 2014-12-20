from django.conf.urls import patterns, url
from shifts import views


urlpatterns = patterns('',  # NOQA
    url(r'^leaderboard/$', views.LeaderBoardView.as_view(), name='leaderboard'),
    url(r'^app/$', views.ShiftAppView.as_view(), name='shift-app'),
)
