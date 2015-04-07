from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'departments', views.DepartmentViewSet)
router.register(r'roles', views.RoleViewSet)

urlpatterns = router.urls
