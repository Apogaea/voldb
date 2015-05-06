from django import template

from volunteer.apps.accounts.api.v2.serializers import (
    UserSerializer,
)

register = template.Library()


@register.filter(name='serialized_user')
def serialized_user(user):
    return UserSerializer(user).data


@register.filter(name='is_department_admin')
def is_department_admin(user, department):
    return department.user_can_admin(user)
