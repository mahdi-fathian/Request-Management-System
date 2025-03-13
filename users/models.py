# from django.db import models

# # Create your models here.






from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = (
        ('USER', 'کاربر عادی'),
        ('EXPERT', 'کارشناس'),
        ('ADMIN', 'مدیر'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='USER', verbose_name="نقش")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="شماره تلفن")
    department = models.CharField(max_length=100, blank=True, verbose_name="دپارتمان")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.username
    












    