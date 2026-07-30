from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # 1. Registration
    path('register/', views.register, name='register'),
    
    # 2. Login
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # 3. Logout
    path('logout/', views.user_logout, name='logout'),

    # 4. Donor Profile (New: Allows Adopters to view Donor details)
    path('profile/<int:pk>/', views.user_profile, name='user_profile'),
]