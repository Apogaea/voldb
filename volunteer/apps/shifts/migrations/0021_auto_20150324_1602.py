# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0020_auto_20150323_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftslot',
            name='volunteer',
            field=models.ForeignKey(related_name='shift_slots', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
