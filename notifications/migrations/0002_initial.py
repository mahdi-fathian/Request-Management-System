# Generated by Django 5.1.7 on 2025-03-13 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("notifications", "0001_initial"),
        ("requests", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="related_request",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="requests.request",
                verbose_name="درخواست مرتبط",
            ),
        ),
    ]
