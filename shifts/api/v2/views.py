from rest_framework import viewsets
from rest_framework import generics
from rest_framework import views
from rest_framework import response
from rest_framework import exceptions

from shifts.models import (
    Role,
    Shift,
)
from shifts.utils import shifts_as_grid

from shifts.api.v2.serializers import (
    RoleSerializer,
    ShiftSerializer,
)


class RoleViewSet(generics.ListAPIView,
                  viewsets.GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ShiftViewSet(generics.ListAPIView,
                   generics.RetrieveAPIView,
                   generics.UpdateAPIView,
                   viewsets.GenericViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

    def update(self, *args, **kwargs):
        shift = self.get_object()
        if shift.owner and not shift.owner == self.request.user:
            raise exceptions.ParseError("You cannot release other people's shifts")
        return super(ShiftViewSet, self).update(*args, **kwargs)


class GridAPIView(views.APIView):
    def get(self, *args, **kwargs):
        shift_pks = self.request.GET.getlist('s')
        if not shift_pks:
            raise exceptions.ParseError("Must provide shift pks")

        grid_data = tuple(shifts_as_grid(Shift.objects.filter(pk__in=shift_pks)))
        return response.Response(grid_data)
