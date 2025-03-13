# from django.db import models

# # Create your models here.



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    TYPE_CHOICES = [
        ('REQUEST', 'درخواست'),
        ('REVIEW', 'بررسی'),
        ('MEETING', 'جلسه'),
        ('RESOLUTION', 'تصمیم'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="کاربر")
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="نوع اعلان")
    message = models.TextField(verbose_name="پیام")
    related_request = models.ForeignKey('requests.Request', on_delete=models.CASCADE, null=True, blank=True, verbose_name="درخواست مرتبط")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان‌ها"

    def __str__(self):
        return f"{self.notification_type} - {self.user.username}"
    





    