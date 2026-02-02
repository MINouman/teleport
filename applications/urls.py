from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'applications'

router = DefaultRouter()
router.register(r'applications', views.JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]