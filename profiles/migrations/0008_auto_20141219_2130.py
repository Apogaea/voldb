# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20140329_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(related_name='_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
