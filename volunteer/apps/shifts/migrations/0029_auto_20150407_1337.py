# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0028_remove_shift_role'),
    ]

    database_operations = [
        migrations.AlterModelTable('Role', 'departments_role')
    ]

    state_operations = [
        migrations.DeleteModel('Role')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
