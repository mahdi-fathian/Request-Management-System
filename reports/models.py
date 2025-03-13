# from django.db import models

# # Create your models here.






from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان گزارش")
    description = models.TextField(verbose_name="توضیحات")
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تولید کننده")
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ تولید")
    data = models.JSONField(verbose_name="داده‌ها")

    class Meta:
        verbose_name = "گزارش"
        verbose_name_plural = "گزارش‌ها"

    def __str__(self):
        return self.title
    









    