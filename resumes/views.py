from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CareerProfile, Resume, ResumeSection
from .serializers import CareerProfileSerializer, ResumeSerializer

# Create your views here.

class CareerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CareerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CareerProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile_ids = CareerProfile.objects.filter(
            user = self.request.user
        ).values_list('id', flat = True)

        return Resume.objects.filter(profile_id__in=user_profile_ids)
    
    def perform_create(self, serializer):
        profile_id = self.request.data.get('profile')
        try:
            profile = CareerProfile.objects.get(id=profile_id, user=self.request.user)
        except CareerProfile.DoesNotExist:
            return Response(
                {"detail": "Profile not found or doesn't belong to you."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(profile=profile)