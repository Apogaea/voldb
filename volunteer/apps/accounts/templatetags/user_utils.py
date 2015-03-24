from django import template

from volunteer.apps.accounts.api.v2.serializers import (
    UserSerializer,
)

register = template.Library()


@register.filter(name='serialized_user')
def serialized_user(user):
    if user.is_anonymous():
        return {"id": None}
    return UserSerializer(user).data
