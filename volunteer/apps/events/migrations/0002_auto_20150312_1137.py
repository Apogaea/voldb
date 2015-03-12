# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


def create_2014_apogaea_event(apps, schema_editor):
    Shift = apps.get_model('shifts', 'Shift')
    Event = apps.get_model('events', 'Event')

    open_at = timezone.now().replace(
        year=2014, month=3, day=1, hour=0, minute=0, second=0, microsecond=0,
    )
    close_at = timezone.now().replace(
        year=2014, month=6, day=1, hour=0, minute=0, second=0, microsecond=0,
    )
    apogaea_2013 = Event.objects.get_or_create(
        name='Apogaea 2013',
        defaults={
            'registration_open_at': open_at,
            'registration_close_at': close_at,
        },
    )

    Shift.objects.all().update(event=apogaea_2013)

    # Ensure that next migration which removes the nullability of this field
    # will not fail.
    assert not Shift.objects.filter(event__isnull=True).exists()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_2014_apogaea_event)
    ]
