# Generated by Django 4.1.7 on 2023-11-14 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0010_alter_patient_date_of_birth"),
        ("Beds", "0002_bed_patient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bed",
            name="patient",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="patients.patient",
            ),
        ),
    ]