from rest_framework import serializers

from departments.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    lead = serializers.SerializerMethodField()
    liaison = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'description',
            'lead',
            'liaison',
        )

    def get_lead(self, obj):
        return getattr(obj.active_lead, 'pk', None)

    def get_liaison(self, obj):
        if obj.active_liaison:
            return [obj.active_liaison.pk]
        else:
            return []
