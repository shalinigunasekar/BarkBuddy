from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration logic
    path('register/', views.register, name='register'),
    
    # Login logic
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Logout logic (using our custom function)
    path('logout/', views.user_logout, name='logout'),
]