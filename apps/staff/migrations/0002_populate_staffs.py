from django.db import migrations

standard_perms = {'create': 1, 'read': 1,
                 'update': 1, 'destroy': 0,
                 'sign': 0, 'award': 1,
                 'administrate_users': 1}

def reverse_func(apps, schema_editor):
    pass

def forwards_func(apps, schema_editor):

    FacultyStaff = apps.get_model('staff', 'FacultyStaff')
    InstitutionStaff = apps.get_model('staff', 'InstitutionStaff')
    BadgeUser = apps.get_model('badgeuser', 'BadgeUser')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    for user in BadgeUser.objects.all():
        perms = list(Permission.objects.filter(user=user))
        for group in Group.objects.filter(user=user):
            perms += list(group.permissions.all())
        unique_perms = set([perm.codename for perm in perms])
        if 'has_institution_scope' in unique_perms:
            InstitutionStaff.objects.create(user=user, institution=user.institution, **standard_perms)
        if 'has_faculty_scope' in unique_perms:
            for faculty in user.faculty.all():
                FacultyStaff.objects.create(user=user, faculty=faculty, **standard_perms)


class Migration(migrations.Migration):
    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]