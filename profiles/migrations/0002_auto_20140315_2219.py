# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='playa_name',
            new_name='display_name',
        ),
        migrations.AlterField(
            model_name='profile',
            name='camps',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='art',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
