from collections import OrderedDict

from rest_framework import response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import pagination

from volunteer.apps.departments.models import (
    Department,
    Role,
)

from volunteer.apps.departments.api.v2.serializers import (
    RoleSerializer,
    DepartmentSerializer,
)


class PassThroughPaginator(pagination.BasePagination):
    def get_paginated_response(self, data):
        return response.Response(OrderedDict([
            ('count', len(data)),
            ('next', None),
            ('previous', None),
            ('results', data)
        ]))

    def paginate_queryset(self, queryset, *args, **kwargs):
        return queryset


class DepartmentViewSet(generics.ListAPIView,
                        viewsets.GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = PassThroughPaginator


class RoleViewSet(generics.ListAPIView,
                  generics.RetrieveAPIView,
                  viewsets.GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
