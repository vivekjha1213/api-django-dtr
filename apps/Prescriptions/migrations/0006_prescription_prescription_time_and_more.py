from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Prescriptions", "0005_prescription_client"),
    ]

    operations = [
        migrations.AddField(
            model_name="prescription",
            name="prescription_time",
            field=models.TimeField(auto_now_add=True),  
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="prescription",
            name="prescription_date",
            field=models.DateField(),
        ),
    ]
