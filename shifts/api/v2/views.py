from rest_framework import viewsets
from rest_framework import generics
from rest_framework import views
from rest_framework import response
from rest_framework import exceptions

from shifts.models import Shift
from shifts.utils import shifts_as_grid

from shifts.api.v2.serializers import ShiftSerializer


class ShiftViewSet(generics.ListAPIView,
                   viewsets.GenericViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class GridAPIView(views.APIView):
    def get(self, *args, **kwargs):
        shift_pks = self.request.GET.getlist('s')
        if not shift_pks:
            raise exceptions.ParseError("Must provide shift pks")

        grid_data = tuple(shifts_as_grid(Shift.objects.filter(pk__in=shift_pks)))
        return response.Response(grid_data)
