# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_role_id(apps, schema_editor):
    Shift = apps.get_model('shifts', 'Shift')

    num_shifts = Shift.objects.count()
    num_updated = Shift.objects.update(role_id=models.F('tmp_role_id'))

    if num_shifts != num_updated:
        raise ValueError("something is wrong")
    if Shift.objects.filter(role_id__isnull=True).exists():
        raise ValueError("something is wrong")


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0030_shift_role'),
    ]

    operations = [
        migrations.RunPython(populate_role_id)
    ]
