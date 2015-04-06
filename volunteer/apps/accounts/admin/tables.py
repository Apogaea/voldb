import django_tables2 as tables
from django_tables2 import (
    A,
)

from volunteer.apps.profiles.models import Profile


class ProfileTable(tables.Table):
    id = tables.Column(accessor=A('user.pk'), verbose_name="id")
    email = tables.Column(accessor=A('user.email'))
    created_at = tables.DateColumn(accessor=A('user.date_joined'))
    last_login = tables.DateColumn(accessor=A('user.last_login'))
    display_name = tables.LinkColumn('admin:user-detail', kwargs={'pk': A('user.pk')})

    class Meta:
        model = Profile
        template = 'admin/partials/table.html'
        fields = (
            'id',
            'display_name',
            'full_name',
            'email',
            'phone',
            'has_ticket',
            'created_at',
            'last_login',
        )
        attrs = {
            'class': 'table table-striped table-bordered',
        }
