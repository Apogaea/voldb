from rest_framework import response
from rest_framework import exceptions
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import detail_route

from volunteer.apps.shifts.models import (
    Role,
    Shift,
    ShiftSlot,
)

from volunteer.apps.shifts.api.v2.serializers import (
    RoleSerializer,
    ShiftSerializer,
    ShiftSlotSerializer,
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
        shift = self.get_object()
        if shift.is_claimable_by_user(self.request.user):
            shift_slot = shift.slots.create(volunteer=self.request.user)
            serializer = ShiftSlotSerializer(shift_slot)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise exceptions.PermissionDenied("You are not allowed to claim this shift")


class ShiftSlotViewSet(generics.ListAPIView,
                       generics.RetrieveAPIView,
                       viewsets.GenericViewSet):
    queryset = ShiftSlot.objects.all()
    serializer_class = ShiftSlotSerializer
