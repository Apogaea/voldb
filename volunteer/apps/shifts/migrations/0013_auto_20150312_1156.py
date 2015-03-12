# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0012_auto_20150312_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='event',
            field=models.ForeignKey(related_name='shifts', on_delete=django.db.models.deletion.PROTECT, to='events.Event'),
            preserve_default=True,
        ),
    ]
