# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20150415_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(help_text=b'This will be the name that is publicly displayed to other users when browsing shifts', max_length=64, unique=True, null=True),
            preserve_default=True,
        ),
    ]
