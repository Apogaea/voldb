from rest_framework.routers import DefaultRouter

from shifts.api.views import ShiftModelViewSet

router = DefaultRouter()

router.register(r'shifts', ShiftModelViewSet)

urlpatterns = router.urls
