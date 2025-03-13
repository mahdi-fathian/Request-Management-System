from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, RequestViewSet, ExpertReviewViewSet, MeetingViewSet, ResolutionViewSet, RequestHistoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'reviews', ExpertReviewViewSet)
router.register(r'meetings', MeetingViewSet)
router.register(r'resolutions', ResolutionViewSet)
router.register(r'history', RequestHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]





