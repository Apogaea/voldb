from django.contrib.auth import get_user_model

import django_tables2 as tables
from django_tables2 import (
    A,
)

User = get_user_model()


class UserTable(tables.Table):
    display_name = tables.LinkColumn(
        'admin:user-detail',
        kwargs={'pk': A('pk')},
        accessor=A('profile.display_name'),
    )
    is_admin = tables.BooleanColumn()

    class Meta:
        model = User
        template = 'admin/partials/table.html'
        fields = (
            'id',
            'display_name',
            'profile.full_name',
            'email',
            'profile.phone',
            'profile.has_ticket',
            'is_active',
            'is_admin',
            'date_joined',
            'last_login',
        )
        attrs = {
            'class': 'table table-striped table-bordered',
        }
