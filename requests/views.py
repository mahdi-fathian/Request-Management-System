# from django.shortcuts import render

# # Create your views here.





from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Request, ExpertReview, Meeting, Resolution, RequestHistory
from .serializers import CategorySerializer, RequestSerializer, ExpertReviewSerializer, MeetingSerializer, ResolutionSerializer, RequestHistorySerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name']

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'category', 'submitted_by']
    search_fields = ['title', 'description']
    ordering_fields = ['submitted_at', 'updated_at', 'priority']

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)
        RequestHistory.objects.create(request=serializer.instance, changed_by=self.request.user, change_description="درخواست جدید ثبت شد")

    def perform_update(self, serializer):
        old_status = self.get_object().status
        serializer.save()
        if old_status != serializer.instance.status:
            RequestHistory.objects.create(request=serializer.instance, changed_by=self.request.user, change_description=f"وضعیت از {old_status} به {serializer.instance.status} تغییر کرد")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def assign_expert(self, request, pk=None):
        req = self.get_object()
        expert_id = request.data.get('expert_id')
        try:
            expert = User.objects.get(id=expert_id, role='EXPERT')
            req.assigned_experts.add(expert)
            RequestHistory.objects.create(request=req, changed_by=request.user, change_description=f"کارشناس {expert.username} اختصاص یافت")
            return Response({'status': 'expert assigned'})
        except User.DoesNotExist:
            return Response({'error': 'Expert not found'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_expert(self, request, pk=None):
        req = self.get_object()
        expert_id = request.data.get('expert_id')
        try:
            expert = User.objects.get(id=expert_id, role='EXPERT')
            req.assigned_experts.remove(expert)
            RequestHistory.objects.create(request=req, changed_by=request.user, change_description=f"کارشناس {expert.username} حذف شد")
            return Response({'status': 'expert removed'})
        except User.DoesNotExist:
            return Response({'error': 'Expert not found'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        req = self.get_object()
        if request.user.role != 'EXPERT':
            return Response({'error': 'Only experts can review'}, status=403)
        review_text = request.data.get('review_text')
        score = request.data.get('score', 0)
        if not review_text:
            return Response({'error': 'Review text is required'}, status=400)
        review = ExpertReview.objects.create(request=req, expert=request.user, review_text=review_text, score=score)
        req.status = 'UNDER_REVIEW'
        req.save()
        RequestHistory.objects.create(request=req, changed_by=request.user, change_description="بررسی جدید ثبت شد")
        return Response(ExpertReviewSerializer(review).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def schedule_meeting(self, request, pk=None):
        req = self.get_object()
        if request.user.role != 'ADMIN':
            return Response({'error': 'Only admins can schedule meetings'}, status=403)
        meeting_date = request.data.get('meeting_date')
        notes = request.data.get('notes', '')
        attendees = request.data.get('attendees', [])
        if not meeting_date:
            return Response({'error': 'Meeting date is required'}, status=400)
        meeting = Meeting.objects.create(request=req, meeting_date=meeting_date, notes=notes)
        meeting.attendees.set(attendees)
        req.status = 'MEETING_SCHEDULED'
        req.save()
        RequestHistory.objects.create(request=req, changed_by=request.user, change_description="جلسه برنامه‌ریزی شد")
        return Response(MeetingSerializer(meeting).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resolve(self, request, pk=None):
        req = self.get_object()
        if request.user.role != 'ADMIN':
            return Response({'error': 'Only admins can resolve requests'}, status=403)
        resolution_text = request.data.get('resolution_text')
        if not resolution_text:
            return Response({'error': 'Resolution text is required'}, status=400)
        if hasattr(req, 'resolution'):
            return Response({'error': 'Request already resolved'}, status=400)
        resolution = Resolution.objects.create(request=req, resolution_text=resolution_text, approved_by=request.user)
        req.status = 'RESOLVED'
        req.save()
        RequestHistory.objects.create(request=req, changed_by=request.user, change_description="درخواست حل شد")
        return Response(ResolutionSerializer(resolution).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        req = self.get_object()
        if request.user.role != 'ADMIN':
            return Response({'error': 'Only admins can reject requests'}, status=403)
        reason = request.data.get('reason', 'بدون دلیل')
        req.status = 'REJECTED'
        req.save()
        RequestHistory.objects.create(request=req, changed_by=request.user, change_description=f"درخواست رد شد: {reason}")
        return Response({'status': 'request rejected', 'reason': reason})

class ExpertReviewViewSet(viewsets.ModelViewSet):
    queryset = ExpertReview.objects.all()
    serializer_class = ExpertReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['request', 'expert']
    search_fields = ['review_text']
    ordering_fields = ['reviewed_at']

    def perform_create(self, serializer):
        serializer.save(expert=self.request.user)

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['request']
    ordering_fields = ['meeting_date', 'created_at']

class ResolutionViewSet(viewsets.ModelViewSet):
    queryset = Resolution.objects.all()
    serializer_class = ResolutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['request']
    ordering_fields = ['resolved_at']

    def perform_create(self, serializer):
        serializer.save(approved_by=self.request.user)

class RequestHistoryViewSet(viewsets.ModelViewSet):
    queryset = RequestHistory.objects.all()
    serializer_class = RequestHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['request']
    ordering_fields = ['changed_at']

    def perform_create(self, serializer):
        serializer.save(changed_by=self.request.user)





        