# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0027_auto_20150407_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='role',
        ),
    ]
