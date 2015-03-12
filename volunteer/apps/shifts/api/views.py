from rest_framework import viewsets
from rest_framework import mixins

from shifts.models import Shift
from shifts.serializers import ShiftSerializer


class ShiftModelViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    model = Shift
    serializer_class = ShiftSerializer
