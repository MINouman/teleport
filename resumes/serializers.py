from rest_framework import serializers
from .models import CareerProfile, Resume

# class CareerProfileSerializer(serializers.ModelSerializer):
#     resume_count = serializers.IntegerField(source='resumes.count', read_only=True)
    
#     class Meta:
#         model = CareerProfile
#         fields = [
#             'id', 'user', 'title', 'target_role', 'target_industry',
#             'target_location', 'target_salary_min', 'target_salary_max',
#             'is_active', 'created_at', 'updated_at', 'resume_count'
#         ]
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at']
class CareerProfileSerializer(serializers.ModelSerializer):
    resume_count = serializers.IntegerField(source='resumes.count', read_only=True)
    
    class Meta:
        model = CareerProfile
        fields = [
            'id', 'user', 'title', 'is_active', 
            'created_at', 'updated_at', 'resume_count'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class ResumeSerializer(serializers.ModelSerializer):
    profile_title = serializers.CharField(source='profile.title', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = [
            'id', 'profile', 'profile_title', 'title', 'format', 'version',
            'content', 'file', 'file_url', 'parsed_text', 'skills_extracted',
            'is_primary', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'version', 'parsed_text', 'skills_extracted', 
                           'created_at', 'updated_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None
    
    def validate(self, data):
        request = self.context.get('request')
        if request and data.get('profile'):
            if data['profile'].user != request.user:
                raise serializers.ValidationError(
                    "You can only create resumes for your own profiles"
                )
        return data
    

class ResumeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['profile', 'version_label', 'format_type', 'content', 'file']
    def validate(self, data):
        request = self.context.get('request')
        if data.get('profile') and data['profile'].user != request.user:
            raise serializers.ValidationError(
                "You can only create resumes for your own profiles"
            )
        
        if data.get('format') == 'upload' and not data.get('file'):
            raise serializers.ValidationError(
                "File is required for upload format"
            )
        
        return data