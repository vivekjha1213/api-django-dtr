# Generated by Django 4.1.7 on 2023-09-24 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Departments", "0003_alter_department_unique_together"),
        ("doctors", "0010_remove_doctor_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="department",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to="Departments.department",
            ),
            preserve_default=False,
        ),
    ]
