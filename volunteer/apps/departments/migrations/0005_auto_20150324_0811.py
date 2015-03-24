# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0004_auto_20141219_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
