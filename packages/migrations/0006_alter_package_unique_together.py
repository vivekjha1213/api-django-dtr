# Generated by Django 4.1.7 on 2023-10-15 08:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("packages", "0005_remove_package_id_package_package_id"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="package",
            unique_together={("package_id", "client")},
        ),
    ]