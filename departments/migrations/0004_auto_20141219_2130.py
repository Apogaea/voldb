# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_auto_20140307_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='active_lead',
            field=models.ForeignKey(related_name='lead', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='department',
            name='active_liaison',
            field=models.ForeignKey(related_name='liason', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
