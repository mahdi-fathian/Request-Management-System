# from django.shortcuts import render

# # Create your views here.

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Report
from .serializers import ReportSerializer
from requests.models import Request, ExpertReview, Meeting, Resolution

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['generated_by']
    ordering_fields = ['generated_at']

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def request_summary(self, request):
        data = {
            'total_requests': Request.objects.count(),
            'pending': Request.objects.filter(status='PENDING').count(),
            'under_review': Request.objects.filter(status='UNDER_REVIEW').count(),
            'meeting_scheduled': Request.objects.filter(status='MEETING_SCHEDULED').count(),
            'resolved': Request.objects.filter(status='RESOLVED').count(),
            'rejected': Request.objects.filter(status='REJECTED').count(),
        }
        report = Report.objects.create(
            title="خلاصه وضعیت درخواست‌ها",
            description="گزارش کلی وضعیت درخواست‌ها",
            generated_by=request.user,
            data=data
        )
        return Response(ReportSerializer(report).data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def expert_performance(self, request):
        experts = User.objects.filter(role='EXPERT')
        data = {expert.username: ExpertReview.objects.filter(expert=expert).count() for expert in experts}
        report = Report.objects.create(
            title="عملکرد کارشناسان",
            description="تعداد بررسی‌های انجام شده توسط هر کارشناس",
            generated_by=request.user,
            data=data
        )
        return Response(ReportSerializer(report).data)
    












    