import functools

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import (
    user_passes_test,
)
from django.core.urlresolvers import reverse_lazy

from authtools.views import DecoratorMixin


def user_is_admin(user):
    if user.is_anonymous():
        return False
    return user.is_admin


admin_required = user_passes_test(
    user_is_admin, login_url=reverse_lazy('admin:login'),
)


AdminRequiredMixin = DecoratorMixin(admin_required)


def anonymous_required(func):
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        if request.user.is_anonymous():
            return func(request, *args, **kwargs)
        return redirect(reverse('dashboard'))
    return inner


AnonymousRequiredMixin = DecoratorMixin(anonymous_required)
