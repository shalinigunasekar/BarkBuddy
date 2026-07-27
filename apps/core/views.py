from django.shortcuts import render
from apps.dogs.models import Dog
from apps.accounts.models import User
from apps.adoption.models import AdoptionRequest
from django.contrib.admin.views.decorators import staff_member_required

# 1. Home Page View
def home(request):
    # Fetch the 6 most recent dogs that are available
    featured_dogs = Dog.objects.filter(is_available=True).order_by('-created_at')[:6]
    
    # Calculate statistics for the "Stats Bar"
    stats = {
        'total_dogs': Dog.objects.count(),
        # Count only requests marked as 'Completed'
        'total_adoptions': AdoptionRequest.objects.filter(status='COMPLETED').count(),
        'total_users': User.objects.count(),
    }
    
    return render(request, 'core/home.html', {
        'featured_dogs': featured_dogs,
        'stats': stats
    })

# 2. About Us Page View
def about(request):
    return render(request, 'core/about.html')

# 3. Contact Page View
def contact(request):
    return render(request, 'core/contact.html')

# 4. Custom Admin Dashboard (For Staff only)
@staff_member_required
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_dogs': Dog.objects.count(),
        'pending_requests': AdoptionRequest.objects.filter(status='PENDING').count(),
        'approved_requests': AdoptionRequest.objects.filter(status='ACCEPTED').count(),
        'recent_dogs': Dog.objects.order_by('-created_at')[:5],
        'recent_users': User.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'core/admin_dashboard.html', context)