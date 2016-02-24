from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'events', views.EventViewSet)

urlpatterns = router.urls  # NOQA
