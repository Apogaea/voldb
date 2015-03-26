# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_shift_minutes(apps, schema_editor):
    Shift = apps.get_model('shifts', 'Shift')

    for shift in Shift.objects.all():
        shift.shift_minutes = shift.shift_length * 60
        shift.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0022_shift_shift_minutes'),
    ]

    operations = [
        migrations.RunPython(populate_shift_minutes)
    ]
