from django.contrib.auth import get_user_model

from rest_framework import serializers

from volunteer.apps.departments.models import Department

User = get_user_model()


class DepartmentSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(
        source='active_lead',
        queryset=User.objects.all(),
    )
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

    def get_liaison(self, obj):
        if obj.active_liaison:
            return [obj.active_liaison.pk]
        else:
            return []
