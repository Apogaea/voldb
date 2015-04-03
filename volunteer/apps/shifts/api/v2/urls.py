from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'shifts', views.ShiftViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'slots', views.ShiftSlotViewSet)

urlpatterns = router.urls  # NOQA
