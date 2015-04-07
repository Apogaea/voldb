# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def preserve_role_id(apps, schema_editor):
    Shift = apps.get_model('shifts', 'Shift')

    num_shifts = Shift.objects.count()
    num_updated = Shift.objects.update(tmp_role_id=models.F('role_id'))

    if num_shifts != num_updated:
        raise ValueError("something is wrong")
    if Shift.objects.filter(tmp_role_id__isnull=True).exists():
        raise ValueError("something is wrong")


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0026_auto_20150407_1334'),
    ]

    operations = [
        migrations.RunPython(preserve_role_id)
    ]
