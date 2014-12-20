from rest_framework import viewsets
from rest_framework import generics

from departments.models import Department

from departments.api.v2.serializers import DepartmentSerializer


class DepartmentViewSet(generics.ListAPIView,
                        viewsets.GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
