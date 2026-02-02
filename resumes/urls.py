from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'resumes'

router = DefaultRouter()
router.register(r'profiles', views.CareerProfileViewSet, basename='profile')
router.register(r'resumes', views.ResumeViewSet, basename='resume')

urlpatterns = [
    path('', include(router.urls)),
]