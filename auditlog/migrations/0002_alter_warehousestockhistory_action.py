# Generated by Django 5.1.2 on 2024-10-19 23:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auditlog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="warehousestockhistory",
            name="action",
            field=models.CharField(max_length=50),
        ),
    ]
