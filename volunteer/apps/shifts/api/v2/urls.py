from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'shifts', views.ShiftViewSet)
router.register(r'roles', views.RoleViewSet)

urlpatterns = router.urls  # NOQA
