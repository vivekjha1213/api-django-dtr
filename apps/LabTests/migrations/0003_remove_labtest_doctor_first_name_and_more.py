# Generated by Django 4.2.4 on 2023-08-19 15:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "LabTests",
            "0002_labtest_doctor_first_name_labtest_doctor_last_name_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="labtest",
            name="doctor_first_name",
        ),
        migrations.RemoveField(
            model_name="labtest",
            name="doctor_last_name",
        ),
        migrations.RemoveField(
            model_name="labtest",
            name="patient_first_name",
        ),
        migrations.RemoveField(
            model_name="labtest",
            name="patient_last_name",
        ),
    ]