# from django.db import models

# # Create your models here.



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

class Request(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'در انتظار'),
        ('UNDER_REVIEW', 'در حال بررسی'),
        ('MEETING_SCHEDULED', 'جلسه برنامه‌ریزی شده'),
        ('RESOLVED', 'حل شده'),
        ('REJECTED', 'رد شده'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'کم'),
        ('MEDIUM', 'متوسط'),
        ('HIGH', 'زیاد'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان درخواست")
    description = models.TextField(verbose_name="توضیحات")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="دسته‌بندی")
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_submitted', verbose_name="ثبت‌کننده")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="وضعیت")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM', verbose_name="اولویت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین به‌روزرسانی")
    assigned_experts = models.ManyToManyField(User, related_name='assigned_requests', blank=True, verbose_name="کارشناسان اختصاص داده شده")

    class Meta:
        verbose_name = "درخواست"
        verbose_name_plural = "درخواست‌ها"

    def __str__(self):
        return self.title

class ExpertReview(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='reviews', verbose_name="درخواست")
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="کارشناس")
    review_text = models.TextField(verbose_name="متن بررسی")
    reviewed_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ بررسی")
    score = models.IntegerField(default=0, verbose_name="امتیاز (0-10)")

    class Meta:
        verbose_name = "بررسی کارشناس"
        verbose_name_plural = "بررسی‌های کارشناسان"

    def __str__(self):
        return f"بررسی {self.request.title} توسط {self.expert.username}"

class Meeting(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='meetings', verbose_name="درخواست")
    meeting_date = models.DateTimeField(verbose_name="تاریخ جلسه")
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")
    attendees = models.ManyToManyField(User, related_name='meetings', verbose_name="حاضران")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "جلسه"
        verbose_name_plural = "جلسات"

    def __str__(self):
        return f"جلسه برای {self.request.title}"

class Resolution(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='resolution', verbose_name="درخواست")
    resolution_text = models.TextField(verbose_name="متن تصمیم")
    resolved_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ تصمیم")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolutions', verbose_name="تأیید کننده")

    class Meta:
        verbose_name = "تصمیم"
        verbose_name_plural = "تصمیمات"

    def __str__(self):
        return f"تصمیم برای {self.request.title}"

class RequestHistory(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='history', verbose_name="درخواست")
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="تغییر دهنده")
    change_description = models.TextField(verbose_name="توضیحات تغییر")
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ تغییر")

    class Meta:
        verbose_name = "تاریخچه درخواست"
        verbose_name_plural = "تاریخچه درخواست‌ها"

    def __str__(self):
        return f"تغییر {self.request.title} در {self.changed_at}"
    









    



