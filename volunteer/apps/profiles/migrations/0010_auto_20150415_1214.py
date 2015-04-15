# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20150415_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(help_text=b'This will be the name that is publicly displayed to other users when browsing shifts', unique=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(help_text=b'Please provide us with your full legal name.', max_length=100),
            preserve_default=True,
        ),
    ]
