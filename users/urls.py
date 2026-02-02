from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'users'

urlpatterns = [
    path('auth/register/',       views.RegisterView.as_view({'post': 'create'}),  name='register'),
    path('auth/login/',          views.LoginView.as_view(),                        name='login'),
    path('auth/token/refresh/',  views.RefreshTokenView.as_view(),                 name='token-refresh'),
    path('auth/logout/',         views.LogoutView.as_view(),                       name='logout'),

    path('users/me/',            views.UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='user-profile'),

    path('users/recruiter-profile/', views.RecruiterProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='recruiter-profile'),
]
