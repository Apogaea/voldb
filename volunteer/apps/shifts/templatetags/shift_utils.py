from django import template

from volunteer.apps.shifts.utils import shifts_as_grid


register = template.Library()


@register.filter(name='as_grid')
def as_grid(shifts):
    return tuple(shifts_as_grid(shifts))
