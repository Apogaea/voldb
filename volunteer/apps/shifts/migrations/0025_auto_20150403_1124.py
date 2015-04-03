# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0024_auto_20150325_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='code',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
