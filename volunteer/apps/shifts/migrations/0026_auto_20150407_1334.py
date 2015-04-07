# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0025_auto_20150403_1124'),
        ('departments', '0006_auto_20150324_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='tmp_role_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='role',
            name='department',
            field=models.ForeignKey(to='departments.Department', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
    ]
