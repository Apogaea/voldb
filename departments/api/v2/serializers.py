from rest_framework import serializers

from departments.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    leads = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'description',
            'lead',
            'liaisons',
        )

    def get_lead(self, obj):
        return getattr(obj.active_lead, 'pk', None)

    def get_liaison(self, obj):
        return [getattr(obj.active_liaison, 'pk', None)]
