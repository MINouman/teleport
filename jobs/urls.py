from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'jobs'

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'postings',  views.JobPostingViewSet, basename='jobposting')

urlpatterns = [
    path('', include(router.urls)),
]