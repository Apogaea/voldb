from rest_framework import viewsets
from rest_framework import generics

from shifts.models import Shift

from shifts.api.v2.serializers import ShiftSerializer


class ShiftViewSet(generics.ListAPIView,
                   viewsets.GenericViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
