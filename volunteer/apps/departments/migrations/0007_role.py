# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0029_auto_20150407_1337'),
        ('departments', '0006_auto_20150324_1001'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('department', models.ForeignKey(related_name='roles', on_delete=django.db.models.deletion.PROTECT, to='departments.Department')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        )
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations),
    ]
