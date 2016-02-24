# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150325_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
