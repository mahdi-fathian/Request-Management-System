# from django.shortcuts import render

# # Create your views here.








from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get('role')
        if role not in dict(CustomUser.ROLES):
            return Response({'error': 'Invalid role'}, status=400)
        user.role = role
        user.save()
        return Response(self.get_serializer(user).data)
    










    