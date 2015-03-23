# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0004_remove_shift_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='department',
            field=models.ForeignKey(to='departments.Department', to_field=u'id'),
        ),
    ]
