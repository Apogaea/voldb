# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='shift_length',
            field=models.PositiveSmallIntegerField(default=3),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='shift',
            name='end_time',
        ),
    ]
