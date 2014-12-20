from rest_framework import viewsets
from rest_framework import generics
from rest_framework import pagination
from rest_framework import serializers

from departments.models import Department

from departments.api.v2.serializers import DepartmentSerializer


class PassThroughPaginator(pagination.BasePaginationSerializer):
    results_field = 'data'
    count = serializers.IntegerField()


class DepartmentViewSet(generics.ListAPIView,
                        viewsets.GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_serializer_class = PassThroughPaginator

    def paginate_queryset(self, queryset):
        return {
            'object_list': queryset,
            'count': queryset.count(),
        }