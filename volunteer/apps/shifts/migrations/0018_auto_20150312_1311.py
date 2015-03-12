# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0017_auto_20150312_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name=b'shifthistory',
            name=b'shift',
        ),
        migrations.RemoveField(
            model_name=b'shifthistory',
            name=b'user',
        ),
        migrations.DeleteModel(
            name='ShiftHistory',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='volunteers',
        ),
    ]
