# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                (u'membershiprequest_ptr', models.OneToOneField(auto_created=True, primary_key=True, to_field=u'id', serialize=False, to='organizations.MembershipRequest')),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('organizations.membershiprequest',),
        ),
        migrations.AddField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='organizations.Membership'),
        ),
    ]
