# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150407_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerboseUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('accounts.user',),
        ),
    ]
