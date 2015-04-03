# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shifts', '0015_auto_20150312_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name=b'owner',
        ),
        migrations.AddField(
            model_name='shift',
            name='volunteers',
            field=models.ManyToManyField(related_name='+', through='shifts.ShiftSlot', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shiftslot',
            name='cancelled_at',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shiftslot',
            name='volunteer',
            field=models.ForeignKey(related_name='shifts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='shiftslot',
            unique_together=set([]),
        ),
    ]
