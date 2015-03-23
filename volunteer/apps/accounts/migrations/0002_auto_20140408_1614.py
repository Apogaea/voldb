# encoding: utf8
from django.db import models, migrations


def normalize_email_addresses(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model("accounts", "User")
    dupes = set()
    for user in User.objects.order_by('date_joined'):
        if user.pk in dupes:
            continue
        email = user.email.lower()
        dupes.update(User.objects.filter(
            email__iexact=email,
        ).exclude(pk=user.pk).values_list('pk', flat=True))

    print 'Deleting users {0}'.format(str(dupes))
    User.objects.filter(pk__in=dupes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(normalize_email_addresses),
    ]
