from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from .models import Company, JobPosting
from .serializers import (
    CompanySerializer,
    JobPostingSerializer,
    JobPostingCreateSerializer,
)

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.created_by == request.user


class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'recruiter'


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Company.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsRecruiter()]
        return super().get_permissions()


class JobPostingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobPostingCreateSerializer
        return JobPostingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'recruiter':
            return JobPosting.objects.filter(posted_by=user)
        return JobPosting.objects.filter(status='active')

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsRecruiter()]
        return super().get_permissions()