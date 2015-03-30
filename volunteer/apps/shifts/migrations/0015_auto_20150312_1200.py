# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_shift_slots_for_shifts(apps, schema_editor):
    Shift = apps.get_model('shifts', 'Shift')
    ShiftSlot = apps.get_model('shifts', 'ShiftSlot')

    qs = Shift.objects.filter(owner__isnull=False)
    for shift in qs:
        if ShiftSlot.objects.filter(shift=shift).exists():
            continue
        ShiftSlot.objects.get_or_create(
            shift=shift,
            volunteer=shift.owner,
        )

    # sanity check we aren't going to lose any data when the next migration
    # drops the owner field.
    assert (
        Shift.objects.filter(owner__isnull=False).count() == ShiftSlot.objects.count()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0014_auto_20150312_1200'),
    ]

    operations = [
        migrations.RunPython(create_shift_slots_for_shifts)
    ]
