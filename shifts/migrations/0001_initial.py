# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('department', models.ForeignKey(to_field=u'id', blank=True, to='departments.Department', null=True)),
                ('start_time', models.DateTimeField(verbose_name='shift begins')),
                ('end_time', models.DateTimeField(verbose_name='shift ends')),
                ('owner', models.ForeignKey(to_field=u'id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
