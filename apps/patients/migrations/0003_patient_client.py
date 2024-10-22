# Generated by Django 4.1.7 on 2023-08-22 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Hospitals", "0001_initial"),
        ("patients", "0002_alter_patient_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="client",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="Hospitals.hospital",
            ),
            preserve_default=False,
        ),
    ]
