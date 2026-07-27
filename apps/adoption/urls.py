from django.urls import path
from . import views

# Nickname for the app (Namespacing)
app_name = 'adoption'

urlpatterns = [
    # 1. Page for Adopters to fill the application form
    path('apply/<int:dog_id>/', views.apply_adoption, name='apply'),
    
    # 2. Dashboard for Donors to see incoming requests
    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
    
    # 3. Page for Adopters to see their own sent applications
    path('my-requests/', views.my_requests, name='my_requests'),
    
    # 4. Action URL to Accept or Reject an adoption request (The Fix)
    path('status/<int:req_id>/<str:status>/', views.update_request_status, name='update_status'),
]