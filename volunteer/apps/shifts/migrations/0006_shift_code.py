# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0005_auto_20140308_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='code',
            field=models.CharField(default='', max_length=20, blank=True),
            preserve_default=False,
        ),
    ]
