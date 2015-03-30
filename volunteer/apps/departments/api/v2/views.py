from rest_framework import response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import pagination
from rest_framework.compat import OrderedDict

from volunteer.apps.departments.models import Department

from volunteer.apps.departments.api.v2.serializers import DepartmentSerializer


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
