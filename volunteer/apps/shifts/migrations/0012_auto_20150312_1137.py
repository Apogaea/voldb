# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('shifts', '0011_auto_20141219_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='role',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 18, 37, 19, 917762, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shift',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='event',
            field=models.ForeignKey(related_name='shifts', on_delete=django.db.models.deletion.PROTECT, to='events.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 18, 37, 24, 948795, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shifthistory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 18, 37, 31, 965127, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='role',
            name='department',
            field=models.ForeignKey(related_name='roles', on_delete=django.db.models.deletion.PROTECT, to='departments.Department'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shift',
            name='role',
            field=models.ForeignKey(related_name='shifts', on_delete=django.db.models.deletion.PROTECT, to='shifts.Role'),
            preserve_default=True,
        ),
    ]
