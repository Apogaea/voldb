# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0034_shift_is_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='is_closed',
            field=models.BooleanField(default=False, help_text='This will restrict anyone from claiming slots on this shift.'),
            preserve_default=True,
        ),
    ]
