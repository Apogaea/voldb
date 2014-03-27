# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shifts', '0006_shift_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftHistory',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('shift', models.ForeignKey(to='shifts.Shift', to_field=u'id')),
                ('action', models.CharField(max_length=10, choices=[(u'claim', u'Claim'), (u'release', u'Release')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
