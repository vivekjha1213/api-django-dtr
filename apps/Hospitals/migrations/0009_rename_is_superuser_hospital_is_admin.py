# Generated by Django 4.1.7 on 2023-08-26 12:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Hospitals", "0008_remove_hospital_groups_remove_hospital_is_admin_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="hospital",
            old_name="is_superuser",
            new_name="is_admin",
        ),
    ]