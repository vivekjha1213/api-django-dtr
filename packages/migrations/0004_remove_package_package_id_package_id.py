# Generated by Django 4.1.7 on 2023-10-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("packages", "0003_alter_package_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="package",
            name="package_id",
        ),
        migrations.AddField(
            model_name="package",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=2,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
    ]