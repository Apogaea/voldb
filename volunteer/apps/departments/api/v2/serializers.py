from django.contrib.auth import get_user_model

from rest_framework import serializers

from volunteer.apps.departments.models import Department

User = get_user_model()


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'description',
            'active_lead',
            'active_liaison',
        )
