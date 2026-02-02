from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import JobApplication, ApplicationStatusHistory
from .serializers import (
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
    ApplicationStatusHistorySerializer
)

class JobApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return JobApplicationCreateSerializer
        return JobApplicationSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'job_seeker':
            return JobApplication.objects.filter(applicant=user).select_related(
                'job', 'resume_version'
            ).prefetch_related('status_history')
        
        return JobApplication.objects.filter(
            job__posted_by=user
        ).select_related(
            'applicant', 'job', 'resume_version'
        ).prefetch_related('status_history')
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update application status (recruiters only)"""
        application = self.get_object()
        
        if application.job.posted_by != request.user:
            return Response(
                {"error": "You can only update applications for your job postings"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if not new_status:
            return Response(
                {"error": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_statuses = [choice[0] for choice in JobApplication.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = application.status
        application.status = new_status
        application.save()
        
        ApplicationStatusHistory.objects.create(
            application=application,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user,
            notes=notes
        )
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def add_notes(self, request, pk=None):
        application = self.get_object()
        
        if application.job.posted_by != request.user:
            return Response(
                {"error": "You can only add notes to applications for your job postings"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notes = request.data.get('recruiter_notes')
        if notes is not None:
            application.recruiter_notes = notes
            application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)