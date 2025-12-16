from django.db import migrations


def create_panchayat_and_wards(apps, schema_editor):
    LocalBody = apps.get_model('locations', 'LocalBody')
    Ward = apps.get_model('locations', 'Ward')

    lb, created = LocalBody.objects.get_or_create(name='Example Panchayat', body_type='panchayat')
    # create some wards
    wards = [
        ('North', 1),
        ('South', 2),
        ('East', 3),
        ('West', 4),
        ('Central', 5),
    ]
    for name, number in wards:
        Ward.objects.get_or_create(local_body=lb, number=number, defaults={'name': name})


def remove_panchayat_and_wards(apps, schema_editor):
    LocalBody = apps.get_model('locations', 'LocalBody')
    LocalBody.objects.filter(name='Example Panchayat', body_type='panchayat').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_panchayat_and_wards, remove_panchayat_and_wards),
    ]
