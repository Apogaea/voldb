# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0031_auto_20150407_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='tmp_role_id',
        ),
        migrations.AlterField(
            model_name='shift',
            name='role',
            field=models.ForeignKey(related_name='shifts', on_delete=django.db.models.deletion.PROTECT, to='departments.Role'),
            preserve_default=True,
        ),
    ]
