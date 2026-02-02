from rest_framework import serializers
from .models import JobApplication, ApplicationStatusHistory
from jobs.serializers import JobPostingSerializer
from users.serializers import UserSerializer

class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.email', read_only=True)
    
    class Meta:
        model = ApplicationStatusHistory
        fields = ['id', 'old_status', 'new_status', 'changed_by', 'changed_by_name', 
                  'changed_at', 'notes']
        read_only_fields = ['id', 'changed_at']

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = JobApplication
        fields = ['id', 'applicant', 'applicant_name', 'job', 'job_title', 
                  'resume_version', 'resume_snapshot', 'cover_letter', 'status',
                  'ats_score', 'match_score', 'recruiter_notes', 'applied_at',
                  'updated_at', 'status_history']
        read_only_fields = ['id', 'applicant', 'resume_snapshot', 'applied_at', 
                           'updated_at', 'ats_score', 'match_score']

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'resume_version', 'cover_letter']
    
    def validate(self, data):
        request = self.context.get('request')
        resume = data['resume_version']
        
        if resume.profile.user != request.user:
            raise serializers.ValidationError("You can only apply with your own resumes")
        
        if JobApplication.objects.filter(
            applicant=request.user,
            job=data['job']
        ).exists():
            raise serializers.ValidationError("You have already applied to this job")
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        resume = validated_data['resume_version']
        
        application = JobApplication.objects.create(
            applicant=request.user,
            job=validated_data['job'],
            resume_version=resume,
            resume_snapshot=resume.content,  
            cover_letter=validated_data.get('cover_letter', '')
        )
        
        return application