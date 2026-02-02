from rest_framework import serializers
from .models import CareerProfile, Resume, ResumeSection

class CareerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProfile
        fields = [
            'id',
            'title',
            'summary',
            'is_active',
            'is_public',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResumeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeSection
        fields = [
            'id',
            'section_type',
            'content',
            'order',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class ResumeSerializer(serializers.ModelSerializer):
    sections = ResumeSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id',
            'profile',
            'version_label',
            'format_type',
            'content',
            'latex_source',
            'uploaded_file',
            'generated_pdf',
            'is_active',
            'sections',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'profile', 'generated_pdf', 'sections', 'created_at', 'updated_at'
        ]