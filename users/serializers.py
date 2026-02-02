from rest_framework import serializers
from .models import User, RecruiterProfile

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only = True)

    first_name = serializers.CharField(max_length= 100, required = False, default = '')
    last_name = serializers.CharField(max_length= 100, required = False, default = '')
    role = serializers.ChoiceField(
        choices=['job_seeker', 'recruiter'], 
        default = 'job_seeker'
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            role = validated_data.get('role', 'job_seeker'),
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name',
            'phone',
            'location', 
            'avatar', 
            'role', 
            'is_active', 
            'created_at', 
            'updated_at',
        ]
        read_only_fields = ['id', 'email', 'role', 'created_at', 'updated_at']

class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)

    class Meta:
        model = RecruiterProfile
        fields = [
            'user', 
            'company_name', 
            'company_website', 
            'bio', 
            'created_at',
        ]
        read_only_fields = ['user', 'created_at']