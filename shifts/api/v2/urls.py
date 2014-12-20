from django.conf.urls import patterns, url
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'shifts', views.ShiftViewSet)
router.register(r'roles', views.RoleViewSet)

urlpatterns = patterns(
    '',  # NOQA
    url(r'^shift-grid/$', views.GridAPIView.as_view(), name='shift-grid'),
)

urlpatterns += router.urls
