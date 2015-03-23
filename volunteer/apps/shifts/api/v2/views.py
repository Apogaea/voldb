from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import detail_route

from volunteer.apps.shifts.models import (
    Role,
    Shift,
)

from volunteer.apps.shifts.api.v2.serializers import (
    RoleSerializer,
    ShiftSerializer,
)


class RoleViewSet(generics.ListAPIView,
                  generics.RetrieveAPIView,
                  viewsets.GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ShiftViewSet(generics.ListAPIView,
                   generics.RetrieveAPIView,
                   viewsets.GenericViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

    @detail_route(methods=['post'])
    def claim(self, *args, **kwargs):
        pass
        # shift = self.get_object()  # TODO
