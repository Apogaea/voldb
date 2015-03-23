# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0018_auto_20150312_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='num_slots',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
    ]
