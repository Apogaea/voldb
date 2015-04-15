# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_display_names_unique(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')

    dupe_names = Profile.objects.values(
        'display_name',
    ).annotate(models.Count('display_name')).values(
        'display_name',
    ).order_by().filter(
        display_name__count__gt=1,
    ).values_list('display_name', flat=True)
    for dupe in dupe_names:
        profiles = Profile.objects.order_by('user__date_joined').filter(display_name=dupe)
        primary = profiles[0]
        others = profiles[1:]
        for index, other in enumerate(others, 1):
            other.display_name += "-{0}".format(index)
            other.save()

    dupe_names = Profile.objects.values(
        'display_name',
    ).annotate(models.Count('display_name')).values(
        'display_name',
    ).order_by().filter(
        display_name__count__gt=1,
    ).values_list('display_name', flat=True)
    if dupe_names:
        raise ValueError("Should not be any dupes")


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20141219_2130'),
    ]

    operations = [
        migrations.RunPython(make_display_names_unique)
    ]
