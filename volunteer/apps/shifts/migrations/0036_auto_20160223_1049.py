# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models

DATE_MAP = {
    datetime.date(2015, 6, 5): datetime.date(2016, 7, 3),
    datetime.date(2015, 6, 6): datetime.date(2016, 7, 4),
    datetime.date(2015, 6, 7): datetime.date(2016, 7, 5),
    datetime.date(2015, 6, 9): datetime.date(2016, 7, 7),
    datetime.date(2015, 6, 10): datetime.date(2016, 7, 8),
    datetime.date(2015, 6, 11): datetime.date(2016, 7, 9),
    datetime.date(2015, 6, 12): datetime.date(2016, 7, 10),
    datetime.date(2015, 6, 13): datetime.date(2016, 7, 11),
    datetime.date(2015, 6, 14): datetime.date(2016, 7, 12),
    datetime.date(2015, 6, 15): datetime.date(2016, 7, 13),
}


def convert_start_time(start_time):
    date_2016 = DATE_MAP[start_time.date()]
    return start_time.replace(
        year=date_2016.year,
        month=date_2016.month,
        day=date_2016.day,
    )


def populuate_2016_shifts_from_2015_shifts(apps, schema_editor):
    Shift = apps.get_model('shifts', 'Shift')
    Event = apps.get_model('events', 'Event')

    try:
        apo_2015 = Event.objects.get(name="Apogaea 2015")
        apo_2016 = Event.objects.get(name="Apogaea 2016")
    except Event.DoesNotExist:
        return

    for shift in apo_2015.shifts.all():
        apo_2016.shifts.get_or_create(
            role=shift.role,
            is_closed=shift.is_closed,
            start_time=convert_start_time(shift.start_time),
            shift_minutes=shift.shift_minutes,
            num_slots=shift.num_slots,
            code=shift.code,
        )


def noop(*args, **kwargs):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('shifts', '0035_auto_20150415_1214'),
        ('events', '0004_auto_20150325_1233'),
        ('departments', '0008_auto_20150506_0853'),
    ]

    operations = [
        migrations.RunPython(populuate_2016_shifts_from_2015_shifts, noop)
    ]
