# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0007_role'),
        ('shifts', '0029_auto_20150407_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='role',
            field=models.ForeignKey(related_name='shifts', on_delete=django.db.models.deletion.PROTECT, default=None, to='departments.Role', null=True),
            preserve_default=True,
        ),
    ]
