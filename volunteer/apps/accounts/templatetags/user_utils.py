from django import template


register = template.Library()


@register.filter(name='is_department_admin')
def is_department_admin(user, department):
    return department.user_can_admin(user)
