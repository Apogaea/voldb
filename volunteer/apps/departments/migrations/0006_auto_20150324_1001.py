# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


PREFIXES = (
    'ASS',
    'AMP',
    'BAMF',
    'Board',
    'Cat Herder',
    'Center Camp',
    'Commissary',
    'DMV',
    'DPW',
    'Fire Convergence',
    'Gate',
    'Greener',
    'Greeters',
    'Info Booth',
    'Lamplighters',
    'Parking',
    'Placement',
    'Quartermaster',
    'Radio',
    'Rangers',
    'Signs',
    'Volunteer',
)


SPECIAL_CASES = {
    'Youth Greeters': 'Greeters',
    'Dirt Ranger': 'Rangers',
    'Board Member On Duty': 'Board',
    'Degreeters': 'Greeters',
}


def merge_departments(apps, schema_editor):
    Department = apps.get_model('departments', 'Department')

    # Update role descriptions
    for department in Department.objects.all():
        if department.roles.count() > 1:
            raise ValueError("Unexpected multiple roles for a department:{0}".format(department.pk))
        role = department.roles.get()
        role.description = department.description
        role.save()

    # Group departments
    dept_groups = dict((
        (prefix, []) for prefix in PREFIXES
    ))
    for department in Department.objects.all():
        if department.name in SPECIAL_CASES:
            dept_groups[SPECIAL_CASES[department.name]].append(department)
            continue

        for prefix in PREFIXES:
            if department.name.startswith(prefix):
                dept_groups[prefix].append(department)
                break
        else:
            raise ValueError("Unable to group Department: {0}".format(department.pk))

    # Merge departments
    for department_name, departments in dept_groups.items():
        primary_department = departments[0]
        primary_department.name = department_name
        primary_department.save()
        for department in departments:
            for role in department.roles.all():
                if department.name in SPECIAL_CASES:
                    actual_name = department.name
                elif department.name.startswith(department.name):
                    actual_name = department.name[len(department_name):].strip()
                else:
                    actual_name = department.name
                role.name = actual_name
                role.save()
            department.roles.update(department=primary_department)

    Department.objects.filter(roles__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0020_auto_20150323_2054'),
        ('events', '0002_auto_20150312_1137'),
        ('departments', '0005_auto_20150324_0811'),
    ]

    operations = [
        migrations.RunPython(merge_departments)
    ]
