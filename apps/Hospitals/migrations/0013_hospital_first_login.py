# Generated by Django 4.1.7 on 2023-09-28 08:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Hospitals", "0012_rename_otp_code_hospital_otp"),
    ]

    operations = [
        migrations.AddField(
            model_name="hospital",
            name="first_login",
            field=models.BooleanField(default=True),
        ),
    ]