# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_shift_slots_for_shifts(apps, schema_editor):
    ShiftSlot = apps.get_model('shifts', 'ShiftSlot')
    ShiftHistory = apps.get_model('shifts', 'ShiftHistory')

    # First clear out the ShiftSlots
    ShiftSlot.objects.all().delete()
    assert not ShiftSlot.objects.exists()

    for history in ShiftHistory.objects.order_by('created_at'):
        if history.action == 'claim':
            history.shift.slots.create(
                created_at=history.created_at,
                volunteer=history.user,
            )
        elif history.action == 'release':
            slot = history.shift.slots.filter(
                volunteer=history.user,
                cancelled_at__isnull=True,
            ).order_by('-created_at').first()
            if not slot:
                history.shift.slots.create(
                    created_at=history.created_at,
                    volunteer=history.user,
                    cancelled_at=history.created_at,
                )
            else:
                slot.cancelled_at = history.created_at
                slot.save()
        else:
            raise ValueError("Unknown action")


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0016_auto_20150312_1251'),
    ]

    operations = [
        migrations.RunPython(create_shift_slots_for_shifts)
    ]
