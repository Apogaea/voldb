# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
