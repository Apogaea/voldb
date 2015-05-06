# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0007_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name=b'active_lead',
        ),
        migrations.RemoveField(
            model_name='department',
            name=b'active_liaison',
        ),
        migrations.AddField(
            model_name='department',
            name='leads',
            field=models.ManyToManyField(related_name='departments', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
