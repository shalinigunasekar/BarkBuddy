from django.urls import path
from . import views

# This namespace matches 'notifications:' in your templates
app_name = 'notifications'

urlpatterns = [
    # 1. Notification Center (Main List)
    # Changed name from 'list' to 'notifications' to match {% url 'notifications:notifications' %}
    path('', views.notification_center, name='notifications'),
    
    # 2. Read and Redirect
    path('read/<int:n_id>/', views.read_and_redirect, name='read_and_redirect'),
    
    # 3. Delete Notification
    path('delete/<int:n_id>/', views.delete_notification, name='delete'),
]