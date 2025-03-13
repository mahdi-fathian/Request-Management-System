from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Request, ExpertReview, Meeting, Resolution, RequestHistory 

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class RequestSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField(read_only=True)
    assigned_experts = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    meetings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    resolution = serializers.PrimaryKeyRelatedField(read_only=True)
    history = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'title', 'description', 'category', 'submitted_by', 'submitted_at', 'status', 'priority', 'updated_at', 'assigned_experts', 'reviews', 'meetings', 'resolution', 'history']
        read_only_fields = ['submitted_by', 'submitted_at', 'updated_at']

class ExpertReviewSerializer(serializers.ModelSerializer):
    expert = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ExpertReview
        fields = ['id', 'request', 'expert', 'review_text', 'reviewed_at', 'score']
        read_only_fields = ['expert', 'reviewed_at']

class MeetingSerializer(serializers.ModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    
    class Meta:
        model = Meeting
        fields = ['id', 'request', 'meeting_date', 'notes', 'attendees', 'created_at']
        read_only_fields = ['created_at']

class ResolutionSerializer(serializers.ModelSerializer):
    approved_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Resolution
        fields = ['id', 'request', 'resolution_text', 'resolved_at', 'approved_by']
        read_only_fields = ['resolved_at', 'approved_by']

class RequestHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = RequestHistory
        fields = ['id', 'request', 'changed_by', 'change_description', 'changed_at']
        read_only_fields = ['changed_by', 'changed_at']
















