# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools

from django.db import models, migrations

def group_key(shift):
    return [shift.role.department.pk, shift.role.name, shift.start_time, shift.shift_length]


def merge_shifts(apps, schema_editor):
    Shift = apps.get_model('shifts', 'Shift')

    qs = Shift.objects.all().order_by('role__department', 'role__name', 'start_time', 'shift_length')
    grouped_shifts = [
        (k, list(v))
        for k, v
        in itertools.groupby(qs, group_key)
    ]

    for _, shifts in grouped_shifts:
        primary_shift = shifts[0]
        primary_shift.num_slots = len(shifts)
        primary_shift.save()

        for shift in shifts[1:]:
            shift.slots.update(shift=primary_shift)


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0019_shift_num_slots'),
    ]

    operations = [
        migrations.RunPython(merge_shifts)
    ]
