from django.urls import path
from . import views

app_name = 'adoption'

urlpatterns = [
    # 1. Dashboard for general user activity
    path('dashboard/', views.user_dashboard, name='donor_dashboard'),
    
    # 2. Assessment dashboard for Donors to manage incoming requests (The table in your image)
    path('manage-requests/', views.donor_applications, name='manage_applications'),
    
    # 3. View for Adopters to see their own sent applications
    path('my-requests/', views.my_requests, name='my_requests'), 
    
    # 4. Detailed view of a single adoption application
    path('request/<int:pk>/', views.adoption_request_detail, name='request_detail'),
    
    # 5. Decision Logic (Approve/Reject)
    path('request/<int:pk>/approve/', views.approve_adoption, name='approve'),
    path('request/<int:pk>/reject/', views.reject_adoption, name='reject'),
    
    # 6. The application form for Adopters
    path('apply/<int:dog_id>/', views.apply_adoption, name='apply'),

    # 7. NEW: Logic to delete/remove an application record
    path('application/delete/<int:pk>/', views.delete_application, name='delete_application'),
]