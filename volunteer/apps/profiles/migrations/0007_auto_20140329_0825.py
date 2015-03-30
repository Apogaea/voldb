# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_has_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='has_ticket',
            field=models.BooleanField(default=False, verbose_name='I have a ticket'),
        ),
    ]
