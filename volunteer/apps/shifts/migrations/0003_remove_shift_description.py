# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0002_auto_20140307_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='description',
        ),
    ]
