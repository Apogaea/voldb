# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0010_auto_20141219_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name=b'department',
        ),
        migrations.AlterField(
            model_name='role',
            name='department',
            field=models.ForeignKey(related_name='roles', to='departments.Department'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shift',
            name='role',
            field=models.ForeignKey(related_name='shifts', to='shifts.Role'),
            preserve_default=True,
        ),
    ]
