from django.core.cache import cache

from volunteer.apps.events.utils import get_active_event
from volunteer.apps.accounts.api.v2.serializers import (
    UserSerializer,
)


USER_DATA_CACHE_KEY = 'user-data'


def user_data(request):
    user = request.user

    cache_key = ':'.join((
        USER_DATA_CACHE_KEY,
        user.pk,
    ))

    user_data = cache.get(cache_key)

    if user_data is None:
        active_event = get_active_event(request.session)
        user_data = UserSerializer(user, active_event).data
        cache.set(cache_key, user_data, 60)

    return {
        'USER_DATA': user_data,
    }
