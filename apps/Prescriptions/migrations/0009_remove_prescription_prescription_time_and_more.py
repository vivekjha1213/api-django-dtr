# Generated by Django 4.1.7 on 2023-09-15 06:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Prescriptions", "0008_alter_prescription_prescription_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="prescription",
            name="prescription_time",
        ),
        migrations.AlterField(
            model_name="prescription",
            name="prescription_date",
            field=models.DateTimeField(),
        ),
    ]