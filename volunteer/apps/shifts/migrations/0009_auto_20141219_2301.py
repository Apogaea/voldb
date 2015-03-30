# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0004_auto_20141219_2130'),
        ('shifts', '0008_auto_20141219_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('department', models.ForeignKey(related_name='roles', blank=True, to='departments.Department', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shift',
            name='role',
            field=models.ForeignKey(related_name='shifts', blank=True, to='shifts.Role', null=True),
            preserve_default=True,
        ),
    ]
