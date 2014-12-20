# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0007_shifthistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='department',
            field=models.ForeignKey(related_name='shifts', to='departments.Department'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shift',
            name='owner',
            field=models.ForeignKey(related_name='shifts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shifthistory',
            name='shift',
            field=models.ForeignKey(related_name='history', to='shifts.Shift'),
            preserve_default=True,
        ),
    ]
