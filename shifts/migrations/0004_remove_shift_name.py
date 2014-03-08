# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0003_remove_shift_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='name',
        ),
    ]
