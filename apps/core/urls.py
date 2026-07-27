from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main Home Page
    path('', views.home, name='home'),
    
    # Mission & Vision Page
    path('about/', views.about, name='about'),
    
    # Contact Information Page
    path('contact/', views.contact, name='contact'),
    
    # Staff Analytics Dashboard
    path('admin-stats/', views.admin_dashboard, name='admin_dashboard'),
]