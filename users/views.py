from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .models import User, RecruiterProfile
from .serializers import RegisterSerializer, UserSerializer, RecruiterProfileSerializer

# Create your views here.
class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.role == 'recruiter':
                RecruiterProfile.objects.create(user=user)
            
            return Response(
                UserSerializer(user).data,
                status = status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class LoginView(TokenObtainPairView):
    pass 

class RefreshTokenView(TokenRefreshView):
    pass 

class LogoutView(TokenBlacklistView):
    pass 


class UserProfileViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        return request.user if hasattr(self, 'request') else None
    
    def retrieve (self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def update(self, request, partial = False):
        serializer = self.get_serializer(request.user, data = request.data, partial = partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request):
        return self.update(request, partial = True)


class RecruiterProfileViewSet(viewsets.GenericViewSet):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecruiterProfile.objects.filter(user=self.request.user)

    def retrieve(self, request):
        """Only recruiters have a profile. Return 404 if they don't."""
        try:
            profile = RecruiterProfile.objects.get(user=request.user)
        except RecruiterProfile.DoesNotExist:
            return Response(
                {"detail": "Recruiter profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def update(self, request, partial=False):
        try:
            profile = RecruiterProfile.objects.get(user=request.user)
        except RecruiterProfile.DoesNotExist:
            return Response(
                {"detail": "Recruiter profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request):
        return self.update(request, partial=True)