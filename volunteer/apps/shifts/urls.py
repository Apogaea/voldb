from django.conf.urls import patterns, url

from volunteer.apps.shifts import views


urlpatterns = patterns('',  # NOQA
    url(r'^$', views.GridView.as_view(), name='shifts'),
    url(r'^leaderboard/$', views.LeaderBoardView.as_view(), name='leaderboard'),
)
