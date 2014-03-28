# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20140315_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='camps',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='art',
        ),
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
    ]
