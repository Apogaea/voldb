# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0033_auto_20150407_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='is_closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
