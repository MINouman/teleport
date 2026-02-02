from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import CareerProfile, Resume
from .serializers import (
    CareerProfileSerializer,
    ResumeSerializer,
    ResumeCreateSerializer
)

class CareerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CareerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CareerProfile.objects.filter(
            user=self.request.user
        ).prefetch_related('resumes')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        """Set this profile as the active one"""
        profile = self.get_object()
        
        CareerProfile.objects.filter(user=request.user).update(is_active=False)
        
        profile.is_active = True
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ResumeCreateSerializer
        return ResumeSerializer
    
    def get_queryset(self):
        return Resume.objects.filter(
            profile__user=self.request.user
        ).select_related('profile')
    
    def perform_create(self, serializer):
        resume = serializer.save()
        
        existing_count = Resume.objects.filter(profile=resume.profile).count()
        resume.version = existing_count
        
        if resume.file:
            self._extract_pdf_text(resume)
        
        resume.save()
    
    def _extract_pdf_text(self, resume):
        """Extract text from PDF for search/analysis"""
        try:
            import PyPDF2
            
            with resume.file.open('rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                resume.parsed_text = text[:10000] 
        except Exception as e:
            print(f"PDF extraction failed: {e}")
    
    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """Set this resume as primary for its profile"""
        resume = self.get_object()
        
        Resume.objects.filter(profile=resume.profile).update(is_primary=False)
        
        resume.is_primary = True
        resume.save()
        
        serializer = self.get_serializer(resume)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Create a copy of this resume"""
        original = self.get_object()
        
        new_resume = Resume.objects.create(
            profile=original.profile,
            title=f"{original.title} (Copy)",
            format=original.format,
            content=original.content.copy() if original.content else {},
            parsed_text=original.parsed_text,
            skills_extracted=original.skills_extracted.copy() if original.skills_extracted else []
        )
        
        serializer = self.get_serializer(new_resume)
        return Response(serializer.data, status=status.HTTP_201_CREATED)