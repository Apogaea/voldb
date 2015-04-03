# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


def create_default_event(apps, schema_editor):
    Event = apps.get_model('events', 'Event')

    open_at = timezone.now().replace(
        year=2014, month=3, day=1, hour=0, minute=0, second=0, microsecond=0,
    )
    close_at = timezone.now().replace(
        year=2014, month=5, day=1, hour=0, minute=0, second=0, microsecond=0,
    )

    if not Event.objects.exists():
        Event.objects.create(
            name="Apogaea 2014",
            registration_open_at=open_at,
            registration_close_at=close_at,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150312_1137'),
    ]

    operations = [
        migrations.RunPython(create_default_event)
    ]
