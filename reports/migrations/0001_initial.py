# Generated by Django 5.1.7 on 2025-03-13 13:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="عنوان گزارش")),
                ("description", models.TextField(verbose_name="توضیحات")),
                (
                    "generated_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ تولید"),
                ),
                ("data", models.JSONField(verbose_name="داده\u200cها")),
            ],
            options={
                "verbose_name": "گزارش",
                "verbose_name_plural": "گزارش\u200cها",
            },
        ),
    ]
