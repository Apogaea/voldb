from django.contrib.auth import get_user_model

import django_tables2 as tables
from django_tables2 import (
    A,
)

from volunteer.tables import BootstrapTable

User = get_user_model()


class UserTable(BootstrapTable):
    display_name = tables.LinkColumn(
        'admin:user-detail',
        kwargs={'pk': A('pk')},
        verbose_name='Display Name',
        accessor=A('profile.display_name'),
        order_by='_profile.display_name',
    )
    is_admin = tables.BooleanColumn(
        verbose_name='Admin',
        order_by=('-is_superuser', '-is_staff'),
    )
    full_name = tables.Column(
        accessor=A('profile.full_name'),
        order_by='_profile.full_name',
    )
    phone = tables.Column(
        accessor=A('profile.phone'),
        order_by='_profile.phone',
    )
    has_ticket = tables.BooleanColumn(
        accessor=A('profile.has_ticket'),
        order_by='-_profile.has_ticket',
    )

    class Meta(BootstrapTable.Meta):
        model = User
        fields = (
            'id',
            'display_name',
            'full_name',
            'email',
            'phone',
            'has_ticket',
            'is_active',
            'is_admin',
            'date_joined',
            'last_login',
        )
