# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shifts', '0013_auto_20150312_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shift', models.ForeignKey(related_name='slots', to='shifts.Shift')),
                ('volunteer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='shiftslot',
            unique_together=set([('shift', 'volunteer')]),
        ),
    ]
