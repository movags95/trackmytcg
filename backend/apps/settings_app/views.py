from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserSettings
from .serializers import UserSettingsSerializer


class UserSettingsViewSet(viewsets.ViewSet):
    """Get and update user settings for the hardcoded user"""

    def list(self, request):
        """Get user settings"""
        user = User.objects.first()  # Hardcoded user
        settings, created = UserSettings.objects.get_or_create(user=user)
        serializer = UserSettingsSerializer(settings)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Update user settings"""
        user = User.objects.first()  # Hardcoded user
        settings, created = UserSettings.objects.get_or_create(user=user)
        serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
