# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_role_for_shift(apps, schema_editor):
    Department = apps.get_model('departments', 'Department')
    Shift = apps.get_model('shifts', 'Shift')
    Role = apps.get_model('shifts', 'Role')

    for department in Department.objects.all():
        role = Role.objects.create(
            department=department,
            name="Generated role for: {0}".format(department.name),
            description="This role was generated during the creation of the `Role` model",
        )
        department.shifts.all().update(role=role)

    assert not Shift.objects.filter(role__isnull=True).exists()


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0009_auto_20141219_2301'),
    ]

    operations = [
        migrations.RunPython(create_role_for_shift)
    ]
