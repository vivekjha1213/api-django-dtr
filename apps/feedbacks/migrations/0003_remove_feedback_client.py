# Generated by Django 4.1.7 on 2023-09-22 10:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("feedbacks", "0002_feedback_client"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedback",
            name="client",
        ),
    ]