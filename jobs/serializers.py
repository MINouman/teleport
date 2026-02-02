from rest_framework import serializers
from .models import Company, JobPosting

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'slug',
            'website',
            'logo',
            'description',
            'industry',
            'founded_year',
            'employee_count',
            'is_verified',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'is_verified', 'created_at', 'updated_at']


class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = JobPosting
        fields = [
            'id',
            'company',
            'title',
            'slug',
            'description',
            'status',
            'experience_level',
            'employment_type',
            'location',
            'is_remote',
            'salary_min',
            'salary_max',
            'salary_currency',
            'required_skills',
            'preferred_skills',
            'education_required',
            'max_applications',
            'application_deadline',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'company', 'created_at', 'updated_at']


class JobPostingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            'company',      
            'title',
            'description',
            'status',
            'experience_level',
            'employment_type',
            'location',
            'is_remote',
            'salary_min',
            'salary_max',
            'salary_currency',
            'required_skills',
            'preferred_skills',
            'education_required',
            'max_applications',
            'application_deadline',
        ]

    def validate_company(self, value):
        request = self.context['request']
        if value.created_by != request.user:
            raise serializers.ValidationError(
                "You can only create job postings for your own companies."
            )
        return value