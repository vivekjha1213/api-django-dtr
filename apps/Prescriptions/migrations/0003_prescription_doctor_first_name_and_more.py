# Generated by Django 4.2.4 on 2023-08-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Prescriptions", "0002_rename_doctor_id_prescription_doctor_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="prescription",
            name="doctor_first_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="prescription",
            name="doctor_last_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="prescription",
            name="patient_first_name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="prescription",
            name="patient_last_name",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]