# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20140327_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_ticket',
            field=models.BooleanField(default=False, verbose_name='I have a ticket'),
            preserve_default=False,
        ),
    ]
